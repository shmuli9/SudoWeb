class SudokuGrid:
    allowed_digits = {0, 1, 2, 3, 4, 5, 6, 7, 8}

    def __init__(self, board_size=9):
        self.array = [[-1 for _ in range(board_size)] for __ in range(board_size)]

    def get_row(self, index):
        return set(self.array[index])

    def get_column(self, index):
        column = set()
        for row in self.array:
            column.add(row[index])
        return column

    def get_box(self, index):
        box = set()
        box_column = index % 3  # which box column to find the box in
        box_row = index // 3  # which box row to find the box in

        column_num_max = ((box_column + 1) * 3)
        row_num_max = ((box_row + 1) * 3)

        for row in range(row_num_max - 3, row_num_max):
            for digit in range(column_num_max - 3, column_num_max):
                box.add(self.array[row][digit])
        return box

    def possible_digits(self, row, col):
        """
        Find the possible digits for current cell
        :param row: row index
        :param col: column index
        :return: set of non-conflicting digits
        """

        add = col // 3
        mult = (row // 3) * 3
        box_num = mult + add

        conflicts = self.get_row(row) | self.get_column(col) | self.get_box(box_num)
        possible = self.allowed_digits - conflicts

        return list(possible)

    def __str__(self):
        out = "-----------------------------------\n"
        row_count = 1
        for row in self.array:
            row_count += 1
            for digit in row:
                out += str(digit + 1 if digit is not -1 else "X") + " | "
            out += "\n-----------------------------------\n"
        return out
