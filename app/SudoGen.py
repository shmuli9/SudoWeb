import random
import time
import statistics
from typing import List, Tuple
from multiprocessing import Pool, cpu_count

from app.Sudoku import SudokuGrid


class SudokuGen(SudokuGrid):
    def __init__(self, board_size=9):
        super(SudokuGen, self).__init__(board_size)
        # Pre-compute random digit orders for better performance
        self._digit_orders = [list(range(1, 10)) for _ in range(81)]
        for order in self._digit_orders:
            random.shuffle(order)
        self._order_index = 0

    def generate_board(self):
        """
        Start from top left cell (0,0) place a random digit and then call try_a_digit to recursively run thorugh the rest
        of the board, attemptiong to place random, legal digits, and recursively unwinding and trying the next value if a
        cell down the line becomes impossible to fill
         :return:
        """
        self._order_index = 0  # Reset order index for new board generation
        if self.try_a_digit(0, 0):  # and self.check_board()
            return self

        print(f"Failed to generate board\n{self}")

    def try_a_digit(self, row, column):
        if column == 8:
            next_row = row + 1  # increment row if on last column
            next_col = 0  # set column to 0 if on last column, else increment
        else:
            next_row = row
            next_col = column + 1

        possible = self.possible_digits(row, column)  # get possible digits for current cell
        if not possible:
            self.array[row][column] = None  # if cell is found to be impossible, reset to None and unwind one stack frame
            return False

        # Use pre-computed random orders for better performance
        digit_order = self._digit_orders[self._order_index]
        self._order_index = (self._order_index + 1) % 81

        for p in digit_order:
            if p in possible:
                self.array[row][column] = p  # set cell to random selected value
                if next_row == 9 or self.try_a_digit(next_row, next_col):
                    """Upon reaching the end of board (next_row==9) return True, indicating the final digit was placed 
                    successfully. Otherwise check the next digit (try_a_digit) to see if it fits, returning True if it does.
                    In every other case return False, indicating a cell could not be completed """
                    return True

        self.array[row][column] = None  # if cell is found to be impossible, reset to None and unwind one stack frame
        return False


def test_board_generation(repeat=10):
    boards = []

    # regression test
    if not sanity_check():
        print("Algorithm doesnt appear to be working...cancelling test run")
        grid = SudokuGen()
        grid.generate_board()
        print(grid)
        return

    start = time.time()
    for _ in range(repeat):
        sudoku_grid = SudokuGen()
        boards.append(sudoku_grid.generate_board())
    end = time.time()
    total = (end - start)

    precision = ".4f"

    print(f"{repeat} Sudoku boards generated in {total:{precision}}s.")
    print(f"Average time was {(total / repeat) * 1000:{precision}}ms")

    if repeat <= 10:
        for i in range(len(boards)):
            print(f"Board {i + 1}:")
            print(boards[i])


def sanity_check():
    sudoku_grid = SudokuGen()
    sudoku_grid.generate_board()
    return sudoku_grid.validate_board()

def benchmark_board_generation(iterations: int = 1000) -> Tuple[List[float], float, float, float]:
    """
    Benchmark the Sudoku board generation performance
    :param iterations: Number of boards to generate
    :return: Tuple of (all_times, min_time, max_time, avg_time)
    """
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        grid = SudokuGen()
        grid.generate_board()
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to milliseconds
        
    return times, min(times), max(times), statistics.mean(times)

def generate_single_board(_):
    """Helper function for parallel generation
    :param _: Ignored iterator value from pool.map
    :return: Generated board
    """
    grid = SudokuGen()
    return grid.generate_board()

def generate_boards_parallel(num_boards: int, num_workers: int = None) -> List[SudokuGrid]:
    """
    Generate multiple Sudoku boards in parallel
    :param num_boards: Number of boards to generate
    :param num_workers: Number of worker processes (defaults to CPU count)
    :return: List of generated boards
    """
    if num_workers is None:
        num_workers = cpu_count()
    
    with Pool(processes=num_workers) as pool:
        return pool.map(generate_single_board, range(num_boards))

def benchmark_parallel_generation(iterations: int = 1000, num_workers: int = None) -> Tuple[List[float], float, float, float]:
    """
    Benchmark parallel board generation performance
    :param iterations: Number of boards to generate
    :param num_workers: Number of worker processes
    :return: Tuple of (all_times, min_time, max_time, avg_time)
    """
    start = time.perf_counter()
    generate_boards_parallel(iterations, num_workers)
    end = time.perf_counter()
    total_time = (end - start) * 1000  # Convert to milliseconds
    
    # For parallel benchmarks, we only measure total time since individual times aren't meaningful
    return [total_time], total_time, total_time, total_time

def run_benchmarks(iterations: List[int] = [1, 10, 100, 1000]):
    """
    Run benchmarks with different iteration counts and print results
    :param iterations: List of iteration counts to test
    """
    print("\nRunning Sudoku Board Generation Benchmarks")
    print("==========================================")
    
    print("\nSingle-threaded Performance:")
    print("---------------------------")
    for n in iterations:
        print(f"\nGenerating {n} board{'s' if n > 1 else ''}:")
        times, min_time, max_time, avg_time = benchmark_board_generation(n)
        
        print(f"  Min time: {min_time:.3f}ms")
        print(f"  Max time: {max_time:.3f}ms")
        print(f"  Avg time: {avg_time:.3f}ms")
        if n >= 100:
            p95 = statistics.quantiles(times, n=20)[18]  # 95th percentile
            p99 = statistics.quantiles(times, n=100)[98]  # 99th percentile
            print(f"  P95 time: {p95:.3f}ms")
            print(f"  P99 time: {p99:.3f}ms")
    
    print("\nParallel Performance:")
    print("-------------------")
    num_workers = cpu_count()
    print(f"Using {num_workers} worker processes")
    
    for n in iterations:
        if n < 100:  # Skip small iterations for parallel as overhead would dominate
            continue
        print(f"\nGenerating {n} board{'s' if n > 1 else ''}:")
        times, min_time, max_time, avg_time = benchmark_parallel_generation(n, num_workers)
        total_time = times[0]
        boards_per_second = (n / total_time) * 1000
        
        print(f"  Total time: {total_time:.3f}ms")
        print(f"  Boards/second: {boards_per_second:.1f}")

if __name__ == "__main__":
    run_benchmarks()
