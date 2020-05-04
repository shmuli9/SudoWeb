import random
import time

from app.Sudoku import SudokuGrid

sudoku_grid = SudokuGrid()


def rec_gen_board():
    """
    Start from top left cell (0,0) place a random digit and then call try_a_digit to recursively run thorugh the rest
    of the board, attemptiong to place random, legal digits, and recursively unwinding and trying the next value if a
    cell down the line becomes impossible to fill
     :return:
    """
    possible = sudoku_grid.possible_digits(0, 0)
    for p in random.sample(possible, len(possible)):  # random is required so that each board is (probably) unique
        sudoku_grid.array[0][0] = p
        if try_a_digit(0, 1):
            return sudoku_grid
    print("Failed to generate board")


def try_a_digit(row, column):
    if column == 8:
        next_row = row + 1  # increment row if on last column
        next_col = 0  # set column to 0 if on last column, else increment
    else:
        next_row = row
        next_col = column + 1

    possible = sudoku_grid.possible_digits(row, column)  # get possible digits for current cell

    if possible:
        for p in random.sample(possible, len(possible)):  # random is required so that each board is (probably) unique
            sudoku_grid.array[row][column] = p  # set cell to random selected value
            if next_row == 9 or try_a_digit(next_row, next_col):
                """Upon reaching the end of board (next_row==9) return True, indicating the final digit was placed 
                successfully. Otherwise check the next digit (try_a_digit) to see if it fits, returning True if it does.
                In every other case return False, indicating a cell could not be completed """
                return True

    sudoku_grid.array[row][column] = -1  # if cell is found to be impossible, reset to -1 and unwind one stack frame
    return False


def test_board_generation(repeat=10):
    results = []
    boards = []
    for _ in range(repeat):
        sudoku_grid.__init__()  # reinitialise the SudokuGrid object before each run
        start = time.time()
        # generate_board()
        boards.append(rec_gen_board())
        end = time.time()
        results.append((end - start) * 1000)

    avg = sum(results) / len(results)
    _max = max(results)
    _min = min(results)
    _total = sum(results) / 1000

    precision = ".4f"
    print(
        f"{repeat} Sudoku boards generated in {_total:{precision}}s."
        f"\nAverage time was {avg:{precision}}ms"
        f"\nMax time was {_max:{precision}}ms"
        f"\nMin time was {_min}ms")

    if repeat <= 10:
        for i in range(len(boards)):
            print(f"Board {i + 1}:")
            print(boards[i])

# Old algorithm, non-recursive
# def generate_board():
#     cont = True
#     # count = 1
#
#     while cont:
#         s = SudokuGrid()
#         # count += 1
#         cont = False
#         for i in range(9):
#             for j in range(9):
#                 possible = s.possible_digits(i, j)
#                 if possible:
#                     s.array[i][j] = random.choice(tuple(possible))
#                     continue
#                 cont = True
#                 break
#             if cont: break
#     return s
