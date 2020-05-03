class SudokuGrid:
    _ALLOWED_DIGITS = {0, 1, 2, 3, 4, 5, 6, 7, 8}

    def __init__(self, board_size=9):
        self.array = [[-1 for _ in range(board_size)] for __ in range(board_size)]

    def get_row(self, row, col=None):
        if col is None:
            return set(self.array[row])
        ret = self.array[row][:col] + self.array[row][col + 1:]
        return set(ret)

    def get_column(self, col, row=None):
        column = set()
        for i in range(9):
            if row is None or i is not row:
                column.add(self.array[i][col])
        return column

    def get_box(self, box_num, row_idx=None, col=None):
        box = set()
        box_column = box_num % 3  # which box column to find the box in
        box_row = box_num // 3  # which box row to find the box in

        column_num_max = ((box_column + 1) * 3)
        row_num_max = ((box_row + 1) * 3)

        for row in range(row_num_max - 3, row_num_max):
            for digit in range(column_num_max - 3, column_num_max):
                if (row_idx is None and col is None) or (row is not row_idx and digit is not col):
                    box.add(self.array[row][digit])
        return box

    def possible_digits(self, row=None, col=None):
        """
        Find the possible digits for current cell
        :param row: row index
        :param col: column index
        :return: set of non-conflicting digits
        """
        if row is None or col is None:
            return self._ALLOWED_DIGITS
        return self._ALLOWED_DIGITS - (
                    self.get_row(row) | self.get_column(col) | self.get_box((col // 3) + (row // 3) * 3))

    def check_board(self):
        """
        Returns True if no cell has conflicts with other cells, False otherwise

        todo: check that all digits occur (probably if the board has no conflicts then it is valid, unless using other chars)
        :return:
        """
        for row in range(9):
            for col in range(9):
                add = col // 3
                mult = (row // 3) * 3
                box_num = mult + add

                conflicts = self.get_row(row, col) | self.get_column(col, row) | self.get_box(box_num, row, col)
                if self.array[row][col] in conflicts:
                    return False
        return True

    def __str__(self):
        out = "-------------------------\n"
        row_count = 1
        col_count = 1
        for row in self.array:
            out += "| "
            for digit in row:
                out += str(digit + 1 if digit is not -1 else "X") + " "
                if col_count % 3 == 0:
                    out += "| "
                col_count += 1
            out += "\n"
            if row_count % 3 == 0:
                out += "-------------------------\n"
            row_count += 1
        return out
