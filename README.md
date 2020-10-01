## SudoWeb

I created an algorithm to efficiently create random Sudoku boards.

The algorithm utilises a simple SudokuGrid data structure, purely to store the array of values and to calcuate legal digits for 
individual cells.

The core algorithm is backtracking search (BTS) which recursively steps through the Sudoku board (left to right), placing randomly selected legal 
digits in the cells until the board is full. The algorithm will backtrack if it comes across a cell that cannot be legally 
populated, and attempt to place a different digit in the previous cell, doing so until the board is full.

Originally I used a basic loop, which would restart the entire board every time a cell was found to be impossible to fill.

##### Comparing old (loop) and new (backtracking) algorithms, generating 10,000 Sudoku boards:

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

Depends on numpy

```
python -m venv venv
.\venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python app.py
```