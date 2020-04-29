import random
import time

from app.Sudoku import SudokuGrid


def generate_board():
    cont = True
    count = 1

    start = time.time()
    while cont:
        s = SudokuGrid()
        count += 1
        cont = False
        for i in range(9):
            for j in range(9):
                possible = s.possible_digits(i, j)
                if possible:
                    s.array[i][j] = random.choice(possible)
                    continue
                cont = True
                break
            if cont: break
        end = time.time()

    if s.check_board():
        print(s)
        print(f"Time taken {(end - start) * 1000:.4f}ms, number of tries: {count}")
    else:
        print("Board invalid")

generate_board()
