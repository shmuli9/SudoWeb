## SudoWeb

I created an algorithm to efficiently create random Sudoku boards.

The algorithm utilises a simple SudokuGrid data structure, purely to store the array of values and to calcuate legal digits for 
individual cells.

In this branch the inner data structure is a List of Lists ([[...]...])

The core algorithm is backtracking search (BTS) which recursively steps through the Sudoku board (left to right), 
placing randomly selected legal digits in the cells until the board is full. The algorithm will backtrack if it comes 
across a cell that cannot be legally populated, and attempt to place a different digit in the previous cell, doing so 
until the board is full.

Originally I used a basic loop, which would restart the entire board every time a cell was found to be impossible to fill.

##### Comparing old (restart) and new (backtracking) algorithms, generating 10,000 Sudoku boards:

|           | Time taken to generate 10,000 boards (s) |
|-----------|------------------------------------------|
| Old       |                   ~1120                  |
| New       |                  ~15-18                  |

As can be seen, there is a 60 - 75x speedup in board generation (and approximately the same RAM usage)

|           |            Speedup in algorithms         |
|-----------|------------------------------------------|
| Delta     |                 62 - 75x                 |
| Delta (%) |               6200 - 7500%               |

These figures were obtained on an i7-8550u with 16GB RAM. 
######(On my new machine R7 4800u/16GB 3200MHz RAM, the times are further reduced but I havn't retested my old code so no point putting the new times up)

#### Install

There are no external dependencies, so just run in an IDE or use the following command line script:

`python app.py`