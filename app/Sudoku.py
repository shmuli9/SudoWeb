class SudokuGrid:
    """Base class for Sudoku grid operations and validation"""
    
    _ALLOWED_DIGITS = frozenset({1, 2, 3, 4, 5, 6, 7, 8, 9})
    # Pre-compute box coordinates for O(1) lookups
    _BOX_COORDS = {(i, j): (i // 3) * 3 + j // 3 for i in range(9) for j in range(9)}
    # Pre-compute box cell sets for efficient iteration
    _BOX_CELLS = {box: {(r, c) for r in range(9) for c in range(9) if (r // 3) * 3 + c // 3 == box} for box in range(9)}

    def __init__(self, board_size=9):
        """Initialize an empty Sudoku grid
        :param board_size: Size of the board (default 9x9)
        """
        self.board_size = board_size
        self.array = [[None] * board_size for _ in range(board_size)]
        
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
        :return: Set of non-None values in the row
        """
        if col is not None:
            return {self.array[row][i] for i in range(self.board_size) if i != col and self.array[row][i] is not None}
        return {x for x in self.array[row] if x is not None}

    def get_column(self, col, row=None):
        """
        Returns values in the specified column
        Columns are laid out like so:
        |   |   |   |     |   |
        | 0 | 1 | 2 | ... | 8 |
        |   |   |   |     |   |
        :param col: The column to return
        :param row: If provided, returned values will exclude specified cell
        :return: Set of non-None values in the column
        """
        if row is not None:
            return {self.array[i][col] for i in range(self.board_size) if i != row and self.array[i][col] is not None}
        return {self.array[i][col] for i in range(self.board_size) if self.array[i][col] is not None}

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
        :return: Set of non-None values contained in the box
        """
        if row is not None and col is not None:
            return {self.array[r][c] for r, c in self._BOX_CELLS[box_num] 
                   if (r != row or c != col) and self.array[r][c] is not None}
        return {self.array[r][c] for r, c in self._BOX_CELLS[box_num] 
               if self.array[r][c] is not None}

    def conflicts(self, row, col):
        """
        Find the digits that conflict with the selected cell
        :param row: row index
        :param col: column index
        :return: set of conflicting digits
        """
        box = self._BOX_COORDS[(row, col)]
        return self.get_row(row, col) | self.get_column(col, row) | self.get_box(box, row, col)

    def possible_digits(self, row, col):
        """
        Find the possible digits for a cell by subtracting conflicting digits from the set of allowed digits (1-9)
        :param row: row index
        :param col: column index
        :return: set of non-conflicting digits that can be placed in this cell
        """
        return self._ALLOWED_DIGITS - self.conflicts(row, col)

    def validate_board(self):
        """
        Returns True if no cell has conflicts with other cells, False otherwise
        This is used as a sanity check to ensure the board generation algorithm is working correctly
        """
        return all(self.array[row][col] not in self.conflicts(row, col)
                  for row in range(self.board_size)
                  for col in range(self.board_size)
                  if self.array[row][col] is not None)

    def __str__(self):
        """
        Returns a string representation of the board with proper formatting
        Empty cells are represented by underscores
        """
        return '\n'.join(' '.join(str(x) if x is not None else '_' for x in row) for row in self.array)
