def get_section(i):
    """
    get section indexes for current index

    |012|345|678|

    2 -> (0,3)
    3 -> (3,6)

    :param i:
    :return:
    """
    section = i // 3
    return section * 3, section * 3 + 3


def get_row(puzzle, row):
    """
    Returns contents of the row with current cell
    :param puzzle: sudoku, list of lists
    :param row: row number, 0-based
    :return: list of row contents
    """
    return list(puzzle[row])


def get_column(puzzle, column):
    """
    Returns contents of the column with current cell
    :param puzzle: sudoku, list of lists
    :param column: column number, 0-based
    :return: list of column contents
    """
    return [row[column] for row in puzzle]


def get_region(puzzle, row, column):
    row_section = get_section(row)
    col_section = get_section(column)
    region = [item for row in puzzle[slice(*row_section)] for item in row[slice(*col_section)]]
    return region
