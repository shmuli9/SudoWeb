import numpy as np


class SudokuGrid:
    _ALLOWED_DIGITS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    def __init__(self, board_size=9):
        self.array = np.full(shape=[board_size, board_size], fill_value=None)

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

        row = self.array[row].view()

        if col:
            row[col] = None

        return set(row)

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

        col = self.array[:, col].view()

        if row:
            col[row] = None

        return set(col)

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
        row_max = ((box_row + 1) * 3)

        box = self.array[row_max - 3:row_max, col_max - 3:col_max].flatten()

        if (row and col) and (row_max - 3 < row < row_max) and (col_max - 3 < col < col_max):
            box = box.view()
            box[((row * col) % 9) - 1] = None

        return set(box)  # for why set() is used over np.unique(), see https://stackoverflow.com/a/59111870/13408445

    def possible_digits(self, row=None, col=None):
        """
        Find the possible digits for current cell, by subtracting confliciting digits from set of allowed digits (1-9)
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
                if self.array[row, col] in conflicts:
                    return False
        return True

    def __str__(self):
        # todo: format nicely
        return str(self.array)
