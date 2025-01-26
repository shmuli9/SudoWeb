package sudoku

import (
	"math/rand"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// Generator handles Sudoku board generation
type Generator struct {
	*Grid
	rng *rand.Rand // Per-generator random source for better parallel performance
}

// NewGenerator creates a new Sudoku board generator
func NewGenerator(boardSize int) *Generator {
	return &Generator{
		Grid: NewGrid(boardSize),
		rng:  rand.New(rand.NewSource(time.Now().UnixNano())),
	}
}

// GenerateBoard generates a complete valid Sudoku board
func (g *Generator) GenerateBoard() bool {
	// Reset the board and state
	for row := range g.board {
		for col := range g.board[row] {
			g.Set(row, col, 0)
		}
	}

	// Validate initial state
	if !g.ValidateBoard() {
		return false
	}

	// Fill cells in order
	return g.fillBoard(0, 0)
}

// fillBoard fills the board using sequential filling with optimized digit selection
func (g *Generator) fillBoard(row, col int) bool {
	// Calculate next position
	nextRow, nextCol := row, col+1
	if nextCol == g.boardSize {
		nextRow++
		nextCol = 0
	}

	// If we've filled the entire board, we're done
	if row == g.boardSize {
		return true
	}

	// Get possible digits for current cell
	possible := g.PossibleDigits(row, col)

	// Shuffle possible digits
	for i := len(possible) - 1; i > 0; i-- {
		j := g.rng.Intn(i + 1)
		possible[i], possible[j] = possible[j], possible[i]
	}

	// Try each possible digit
	for _, digit := range possible {
		oldVal := g.Get(row, col)
		g.Set(row, col, digit)
		if g.Get(row, col) == digit && g.fillBoard(nextRow, nextCol) {
			return true
		}
		g.Set(row, col, oldVal)
	}

	return false
}

// workerPool represents a pool of reusable generators
type workerPool struct {
	generators chan *Generator
}

// newWorkerPool creates a new pool of generators
func newWorkerPool(size int) *workerPool {
	pool := &workerPool{
		generators: make(chan *Generator, size),
	}
	// Pre-create generators
	for i := 0; i < size; i++ {
		pool.generators <- NewGenerator(9)
	}
	return pool
}

// get retrieves a generator from the pool
func (p *workerPool) get() *Generator {
	return <-p.generators
}

// put returns a generator to the pool
func (p *workerPool) put(g *Generator) {
	p.generators <- g
}

// GenerateBoards generates multiple Sudoku boards using available CPU cores
func GenerateBoards(count int) ([]*Grid, time.Duration) {
	start := time.Now()
	boards := make([]*Grid, count)

	// Determine optimal number of workers based on CPU cores and workload
	numCPU := runtime.NumCPU()
	numWorkers := numCPU * 4 // Over-subscribe more for better CPU utilization

	// For small counts, don't create more workers than needed
	if count < numWorkers {
		numWorkers = count
	}

	// Create generator pool
	pool := newWorkerPool(numWorkers)

	// Create work distribution channels with optimal buffer sizes
	batchSize := max(1, min(50, count/numWorkers)) // Smaller batches for better load balancing
	jobs := make(chan workBatch, numWorkers*4)     // Larger buffer for smoother scheduling
	results := make(chan boardResult, count)

	// Create a WaitGroup for worker synchronization
	var wg sync.WaitGroup
	wg.Add(numWorkers)

	// Track completed boards for work stealing
	var completed int32

	// Start worker pool
	for i := 0; i < numWorkers; i++ {
		go func(workerID int) {
			defer wg.Done()
			workerBatch(jobs, results, &completed, count, pool)
		}(i)
	}

	// Distribute work in batches
	for start := 0; start < count; start += batchSize {
		end := start + batchSize
		if end > count {
			end = count
		}
		jobs <- workBatch{start: start, end: end}
	}
	close(jobs)

	// Wait for all workers to complete
	wg.Wait()
	close(results)

	// Collect results
	for result := range results {
		boards[result.index] = result.board
	}

	return boards, time.Since(start)
}

type workBatch struct {
	start, end int
}

type boardResult struct {
	index int
	board *Grid
}

// workerBatch processes batches of board generations with work stealing
func workerBatch(jobs <-chan workBatch, results chan<- boardResult, completed *int32, total int, pool *workerPool) {
	// Get a generator from the pool
	gen := pool.get()
	defer pool.put(gen)

	for batch := range jobs {
		for i := batch.start; i < batch.end; i++ {
			// Check if we've completed all boards (work stealing optimization)
			if atomic.LoadInt32(completed) >= int32(total) {
				return
			}

			// Try to generate a board
			if gen.GenerateBoard() {
				results <- boardResult{index: i, board: gen.Grid}
				atomic.AddInt32(completed, 1)

				// Create a new grid for the next iteration, reusing memory
				gen.Grid = NewGrid(9)
			} else {
				// If generation failed, retry with a new grid
				gen.Grid = NewGrid(9)
				i-- // Retry the same index
			}
		}
	}
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

// StreamBoards generates boards and streams them through a channel instead of storing them in memory
func StreamBoards(count int) (<-chan *Grid, chan struct{}) {
	boards := make(chan *Grid, 10000)
	done := make(chan struct{})

	go func() {
		defer close(boards)
		defer close(done)

		numCPU := runtime.NumCPU()
		numWorkers := numCPU * 8
		pool := newWorkerPool(numWorkers)

		var wg sync.WaitGroup
		wg.Add(numWorkers)

		// Shared counter for all workers
		var completed int32

		// Channel for distributing work
		jobs := make(chan struct{}, numWorkers*8)

		// Start workers
		for i := 0; i < numWorkers; i++ {
			go func() {
				defer wg.Done()
				gen := pool.get()
				defer pool.put(gen)

				for range jobs {
					// Try to increment counter, exit if we've hit the limit
					if atomic.AddInt32(&completed, 1) > int32(count) {
						atomic.AddInt32(&completed, -1) // Undo the increment
						return
					}

					// Generate and send board
					if gen.GenerateBoard() {
						boards <- gen.Grid.Clone()
					} else {
						atomic.AddInt32(&completed, -1) // Failed generation
						gen.Grid = NewGrid(9)
						// Put the job back
						select {
						case jobs <- struct{}{}:
						default:
							// If channel is full, just continue
						}
					}
				}
			}()
		}

		// Fill job channel
		for i := 0; i < count; i++ {
			jobs <- struct{}{}
		}
		close(jobs)

		// Wait for all workers
		wg.Wait()
	}()

	return boards, done
}
