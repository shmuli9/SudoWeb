## SudoWeb

I created an algorithm to efficiently create random Sudoku boards.

The algorithm utilises a simple SudokuGrid data structure, purely to store the array of values and to calcuate legal digits for
individual cells.

The core algorithm is backtracking search (BTS) which recursively steps through the Sudoku board (left to right), placing randomly selected legal
digits in the cells until the board is full. The algorithm will backtrack if it comes across a cell that cannot be legally
populated, and attempt to place a different digit in the previous cell, doing so until the board is full.

Originally I used a basic loop, which would restart the entire board every time a cell was found to be impossible to fill.

#### Installation & Usage

##### Python Version

Requirements:

- Python 3.x
- numpy

Setup:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Run the generator
python app.py  # Generates 10,000 boards by default
```

##### Go Version

Requirements:

- Go 1.21 or later

Setup and Usage:

```bash
# Build the binary
go build -o bin/sudoweb cmd/sudoweb/main.go

# Generate a single board
./bin/sudoweb

# Generate multiple boards
./bin/sudoweb -n 10000

# Run benchmarks
go test -bench=. ./...  # Run all benchmarks
go test -bench=GenerateBoard ./...  # Run specific benchmark
go test -bench=. -benchmem ./...  # Include memory allocation stats
```

#### Benchmark Results

Comparing algorithms, generating 10,000 Sudoku boards:

| Implementation              | Time (seconds) | Boards/second |
| --------------------------- | -------------- | ------------- |
| Python (loop)               | ~1120          | ~9            |
| Python (BTS)                | ~10.5          | ~952          |
| Python (optimized)          | ~0.654         | ~1,530        |
| Python (optimized parallel) | ~0.128         | ~7,840        |
| Go (BTS)                    | ~1.3           | ~7,625        |
| Go (BTS parallel)           | ~0.46          | ~21,668       |
| Go (optimized)              | ~0.022         | ~45,000       |
| Go (optimized parallel)     | ~0.006         | ~164,000      |

Performance improvements:

- Python BTS vs Loop: ~106x speedup
- Python optimized vs BTS: ~1.6x speedup
- Python optimized vs Loop: ~170x speedup
- Python parallel vs single-threaded: ~5.1x speedup
- Go vs Python optimized: ~5x speedup
- Go parallel vs Python parallel: ~21x speedup
- Go parallel vs single-threaded: ~2.8x speedup
- Go parallel vs Python Loop: ~2,407x speedup
- Go optimized vs original Go: ~30x speedup
- Go optimized parallel vs original parallel: ~14x speedup

Recent optimizations that led to significant performance improvements:

#### Python Optimizations (~170x vs original Python, ~870x with parallel)

1. Data Structure Improvements:

   - Replaced NumPy arrays with native Python lists
   - Cached box calculations and coordinates
   - Optimized set operations for conflict checking

2. Algorithm Enhancements:

   - Pre-computed random digit orders
   - Early returns for impossible cells
   - Efficient backtracking state management

3. Parallel Processing:
   - Multi-process worker pool using CPU cores
   - Efficient work distribution
   - Minimal inter-process communication

#### Go Optimizations (~30x vs original Go)

1. Pre-computed State Tracking:

   - Maintain separate boolean arrays for rows, columns, and boxes
   - O(1) conflict checking instead of scanning board regions
   - Immediate conflict detection in cell updates

2. Memory Optimizations:

   - Pre-allocated arrays for possible digits and conflicts
   - Efficient state management during backtracking
   - Reduced allocations in hot paths

3. Algorithm Improvements:

   - Fast path for row conflicts (most common case)
   - Optimized digit shuffling using Fisher-Yates
   - Better state preservation during backtracking

4. Parallel Processing Enhancements:
   - Increased worker pool size for better CPU utilization
   - Optimized batch sizes for load balancing
   - Improved work stealing for better resource usage
