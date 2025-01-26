package sudoku

// Grid represents a Sudoku grid
type Grid struct {
	board     [][]int
	boardSize int
	possible  []int    // Pre-allocated array for possible digits
	rows      [][]bool // Pre-computed state of used digits in each row
	cols      [][]bool // Pre-computed state of used digits in each column
	boxes     [][]bool // Pre-computed state of used digits in each box
}

// NewGrid creates a new empty Sudoku grid
func NewGrid(boardSize int) *Grid {
	// Create the board with separate rows for better CPU cache behavior
	board := make([][]int, boardSize)
	for i := range board {
		board[i] = make([]int, boardSize)
	}

	// Create pre-computed state arrays
	rows := make([][]bool, boardSize)
	cols := make([][]bool, boardSize)
	boxes := make([][]bool, boardSize)
	for i := range rows {
		rows[i] = make([]bool, 10) // 0-9 for easy indexing
		cols[i] = make([]bool, 10)
		boxes[i] = make([]bool, 10)
	}

	return &Grid{
		board:     board,
		boardSize: boardSize,
		possible:  make([]int, 0, 9), // Pre-allocate possible digits array
		rows:      rows,
		cols:      cols,
		boxes:     boxes,
	}
}

// Clone creates a deep copy of the grid
func (g *Grid) Clone() *Grid {
	newGrid := NewGrid(g.boardSize)
	// Copy board data
	for i := range g.board {
		copy(newGrid.board[i], g.board[i])
	}
	// Copy state arrays
	for i := range g.rows {
		copy(newGrid.rows[i], g.rows[i])
		copy(newGrid.cols[i], g.cols[i])
		copy(newGrid.boxes[i], g.boxes[i])
	}
	// Copy possible digits array
	newGrid.possible = make([]int, len(g.possible))
	copy(newGrid.possible, g.possible)
	return newGrid
}

// PossibleDigits returns the set of possible digits for a cell
func (g *Grid) PossibleDigits(row, col int) []int {
	// Reset and reuse pre-allocated array
	g.possible = g.possible[:0]

	// Get box index
	boxIdx := (row/3)*3 + col/3

	// Add non-conflicting digits using pre-computed state
	for digit := 1; digit <= 9; digit++ {
		if !g.rows[row][digit] && !g.cols[col][digit] && !g.boxes[boxIdx][digit] {
			g.possible = append(g.possible, digit)
		}
	}

	return g.possible
}

// Set sets the value at the given position
func (g *Grid) Set(row, col, value int) {
	// Clear old value's state if it exists
	if old := g.board[row][col]; old != 0 {
		g.rows[row][old] = false
		g.cols[col][old] = false
		g.boxes[(row/3)*3+col/3][old] = false
	}

	// Set new value and update state
	g.board[row][col] = value
	if value != 0 {
		boxIdx := (row/3)*3 + col/3
		// Check for conflicts before setting
		if g.rows[row][value] || g.cols[col][value] || g.boxes[boxIdx][value] {
			// If there's a conflict, don't update the state
			g.board[row][col] = 0
			return
		}
		g.rows[row][value] = true
		g.cols[col][value] = true
		g.boxes[boxIdx][value] = true
	}
}

// Get gets the value at the given position
func (g *Grid) Get(row, col int) int {
	return g.board[row][col]
}

// ValidateBoard checks if the current board state is valid
func (g *Grid) ValidateBoard() bool {
	// Reset all state arrays using range
	for i := range g.rows {
		for j := range g.rows[i] {
			g.rows[i][j] = false
			g.cols[i][j] = false
			g.boxes[i][j] = false
		}
	}

	// Recompute state from board
	for row := range g.board {
		for col := range g.board[row] {
			val := g.board[row][col]
			if val != 0 {
				boxIdx := (row/3)*3 + col/3
				// Check for conflicts
				if g.rows[row][val] || g.cols[col][val] || g.boxes[boxIdx][val] {
					return false
				}
				// Mark digit as used
				g.rows[row][val] = true
				g.cols[col][val] = true
				g.boxes[boxIdx][val] = true
			}
		}
	}

	return true
}
