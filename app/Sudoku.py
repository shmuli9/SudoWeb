class SudokuGrid:
    _ALLOWED_DIGITS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, board_size=9):
        self.board_size = board_size
        self.array = [[None for _ in range(board_size)] for __ in range(board_size)]

    def get_row(self, row, col=None):
        """
        Returns values in the specified row
        Rows are laid out like so:
        -----------
             0
        -----------
             1
        -----------
             2
        -----------
            ...
        -----------
             8
        -----------
        :param row: The row to return
        :param col: If provided, returned values will exclude specified cell
        :return:
        """
        if col is None:
            return set(self.array[row])
        ret = self.array[row][:col] + self.array[row][col + 1:]
        return set(ret)

    def get_column(self, col, row=None):
        """
        Returns values in the specified column
        Columns are laid out like so:
        |   |   |   |     |   |
        | 0 | 1 | 2 | ... | 8 |
        |   |   |   |     |   |
        :param col: The column to return
        :param row: If provided, returned values will exclude specified cell
        :return:
        """
        column = set()
        for i in range(9):
            if row is None or i is not row:
                column.add(self.array[i][col])
        return column

    def get_box(self, box_num, row=None, col=None):
        """
        Returns values in the specified box
        Boxes are laid out like so:
        | 0 | 1 | 2 |
        | 3 | 4 | 5 |
        | 6 | 7 | 8 |
        :param box_num: the box number to fetch
        :param row: row index - if given with col, will omit the specified cell from the returned set
        :param col: column index - if given with row, will omit the specified cell from the returned set
        :return: Set of values contained in the box (8 or 9 values)
        """
        box_column = box_num % 3  # which box column to find the box in
        box_row = box_num // 3  # which box row to find the box in

        col_max = ((box_column + 1) * 3)
        col_min = col_max - 3
        row_max = ((box_row + 1) * 3)

        box = set()
        for r in range(row_max - 3, row_max):
            for c in range(col_min, col_max):
                if (row is None or col is None) or (r is not row and c is not col):
                    box.add(self.array[r][c])
        return box

    def possible_digits(self, row, col):
        """
        Find the possible digits for current cell, by subtracting confliciting digits from set of allowed digits (1-9)
        :param row: row index
        :param col: column index
        :return: set of non-conflicting digits
        """
        return self._ALLOWED_DIGITS - self.conflicts(row, col)

    def conflicts(self, row, col):
        """
        Find the digits that conflict with the selected cell
        :param row: row index
        :param col: column index
        :return: set of conflicting digits
        """
        return self.get_row(row, col) | self.get_column(col, row) | self.get_box((col // 3) + (row // 3) * 3, row, col)

    def validate_board(self):
        """
        Returns True if no cell has conflicts with other cells, False otherwise
        :return:
        """
        for row in range(9):
            for col in range(9):
                if self.array[row][col] in self.conflicts(row, col):
                    return False
        return True

    def __str__(self):
        out = "-------------------------\n"
        row_count = 1
        col_count = 1
        for row in self.array:
            out += "| "
            for digit in row:
                out += str(digit if digit != None else "X") + " "
                if col_count % 3 == 0:
                    out += "| "
                col_count += 1
            out += "\n"
            if row_count % 3 == 0:
                out += "-------------------------\n"
            row_count += 1
        return out
