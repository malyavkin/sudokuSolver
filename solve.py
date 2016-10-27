def get_section(i):
    """
    get section indexes for current index

    |012|345|678|

    2 -> (0,2)
    3 -> (3,5)

    :param i:
    :return:
    """
    section = i // 3
    return section * 3, section * 3 + 3

class SudokuPuzzle:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def get_row(self, row):
        """
        Returns contents of the row with current cell
        :param row: row number, 0-based
        :return: list of row contents
        """
        return list(self.puzzle[row])

    def get_column(self, column):
        """
        Returns contents of the column with current cell
        :param column: column number, 0-based
        :return: list of column contents
        """
        return [row[column] for row in self.puzzle]

    def get_region(self, row, column):
        row_section = get_section(row)
        col_section = get_section(column)

        new_puzzle = [item for row in self.puzzle[slice(*row_section)] for item in row[slice(*col_section)] ]

        return new_puzzle
