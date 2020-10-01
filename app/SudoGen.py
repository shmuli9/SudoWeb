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
        if try_a_digit(0, 1):  # and sudoku_grid.check_board()
            return sudoku_grid

    print(f"Failed to generate board\n{sudoku_grid}")


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

    sudoku_grid.array[row][column] = None  # if cell is found to be impossible, reset to None and unwind one stack frame
    return False


def test_board_generation(repeat=10):
    boards = []

    start = time.time()
    for _ in range(repeat):
        sudoku_grid.__init__()  # reinitialise the SudokuGrid object before each run
        rec_gen_board()
    end = time.time()
    total = (end - start)

    precision = ".4f"

    print(f"{repeat} Sudoku boards generated in {total:{precision}}s.")
    print(f"Average time was {(total / repeat) * 1000:{precision}}ms")

    if repeat <= 10:
        for i in range(len(boards)):
            print(f"Board {i + 1}:")
            print(boards[i])
