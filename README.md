## SudoWeb

I created an algorithm to efficiently create random Sudoku boards.

The algorithm utilises a simple SudokuGrid data structure, purely to store the array of values and to calcuate legal digits for 
individual cells.

The core algorithm use recursion to step through the Sudoku board (left to right), placing randomly selected legal 
digits in the cells until the board is full. The algorithm will unwind if it comes across a cell that cannot be legally 
populated, and attempt to place a different digit in the previous cell, doing so recursively until the board is full.

Originally I used a basic loop, which would restart the entire board every time a cell was found to be impossible to fill.
Comparing old (loop) and new (recursive), generating 10,000 Sudoku boards:

|           | Time taken to generate 10,000 boards (s) |
|-----------|------------------------------------------|
| Old       |                   ~1120                  |
| New       |                  ~15-18                  |

As can be seen, there is a 60 - 75x speedup in board generation (and approximately the same RAM usage)

|           |            Speedup in algorithms         |
|-----------|------------------------------------------|
| Delta     |                 62 - 75x                 |
| Delta (%) |               6200 - 7500%               |

#### Install

There are no external dependencies, so just run in an IDE or use the following command line script:

`python app.py`