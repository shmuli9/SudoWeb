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

    def get_row_rest(self, row, col):
        ret = self.array[row][:col] + self.array[row][col+1:]
        return set(ret)

    def get_column_rest(self, row, col):
        column = set()
        for i in range(9):
            if i is not row:
                column.add(self.array[i][col])
        return column

    def get_box_rest(self, box_num, row_idx, col):
        box = set()
        box_column = box_num % 3  # which box column to find the box in
        box_row = box_num // 3  # which box row to find the box in

        column_num_max = ((box_column + 1) * 3)
        row_num_max = ((box_row + 1) * 3)

        for row in range(row_num_max - 3, row_num_max):
            for digit in range(column_num_max - 3, column_num_max):
                if row is not row_idx and digit is not col:
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

    def check_board(self):
        for row in range(9):
            for col in range(9):
                add = col // 3
                mult = (row // 3) * 3
                box_num = mult + add

                conflicts = self.get_row_rest(row, col) | self.get_column_rest(row, col) | self.get_box_rest(box_num,
                                                                                                             row, col)
                if self.array[row][col] in conflicts:
                    return False
        return True

    def __str__(self):
        out = "-----------------------------------\n"
        row_count = 1
        for row in self.array:
            row_count += 1
            for digit in row:
                out += str(digit + 1 if digit is not -1 else "X") + " | "
            out += "\n-----------------------------------\n"
        return out
