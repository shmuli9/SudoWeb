import random
import time

from app.Sudoku import SudokuGrid


def generate_board():
    cont = True
    # count = 1

    while cont:
        s = SudokuGrid()
        # count += 1
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
    return s


def test_board_generation(repeat=10):
    results = []
    boards = []
    for _ in range(repeat):
        start = time.time()
        boards.append(generate_board())
        end = time.time()
        results.append((end - start) * 1000)

    avg = sum(results) / len(results)
    _max = max(results)
    _min = min(results)
    _total = sum(results)/1000

    precision = ".4f"
    print(
        f"{repeat} Sudoku boards generated in {_total:{precision}}s."
        f"\nAverage time was {avg:{precision}}ms"
        f"\nMax time was {_max:{precision}}ms"
        f"\nMin time was {_min}ms")

    if repeat <= 10:
        for i in range(len(boards)):
            print(f"Board {i+1}:")
            print(boards[i])


test_board_generation()

# generate_board()
