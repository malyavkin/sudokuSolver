import copy
import sample


def print_puzzle(puzzle):
    delim = "|"
    for i in range(len(puzzle)):
        row = puzzle[i]
        print("{}   {}   {}".format(delim.join(row[0:3]), delim.join(row[3:6]), delim.join(row[6:9])))
        if i % 3 == 2:
            print()


def get_region_indexes(region_number, region_size):
    return region_number*region_size, (region_number+1)*region_size


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
    return get_region_indexes(section, 3)



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


def get_region(puzzle, reg_row, reg_column):
    row_section = get_region_indexes(reg_row, 3)
    col_section = get_region_indexes(reg_column, 3)
    region = [item for row in puzzle[slice(*row_section)] for item in row[slice(*col_section)]]
    return region


def get_region_by_rc(puzzle, row, column):
    row_section = get_section(row)
    col_section = get_section(column)
    region = [item for row in puzzle[slice(*row_section)] for item in row[slice(*col_section)]]
    return region


def get_missing(lst: set, acceptable_values: set) -> set:
    """
    Returns list of values missing from list
    :return: list of values missing from list
    :rtype: set
    :param lst: said list
    :param acceptable_values: all acceptable values (usually digits 1-9)

    """
    return acceptable_values.difference(lst)


def get_empty_cells(puzzle, acceptable_values):
    for i_row in range(len(puzzle)):
        for j_cell in range(len(puzzle[i_row])):
            if puzzle[i_row][j_cell] not in acceptable_values:
                yield i_row, j_cell


def get_empty_cells_in_region(puzzle, acceptable_values, i_min, j_min, i_max, j_max):
    ijs = list(get_empty_cells(puzzle, acceptable_values))
    coords = lambda ij: i_min <= ij[0] < i_max and j_min <= ij[1] < j_max
    return filter(coords, ijs)


def generate_empty_scratch():
    return [[None for j in range(9)] for i in range(9)]

def generate_scratch(puzzle, length, acceptable_values):
    return [["{:^{}}".format(puzzle[i][j], length) if puzzle[i][j] in acceptable_values else "     "
             for j in range(9)] for i in range(9)]

########################################################################################################################
# methods
########################################################################################################################

def find_single_missing(puzzle, acceptable_values):
    """
    Finds all cells with only one variant
    """
    length = 5
    candidates = generate_scratch(puzzle, length, acceptable_values)
    for i, j in get_empty_cells(puzzle, acceptable_values):
        missing_row = get_missing(set(get_row(puzzle, i)), acceptable_values)
        missing_col = get_missing(set(get_column(puzzle, j)), acceptable_values)
        missing_region = get_missing(set(get_region_by_rc(puzzle, i, j)), acceptable_values)
        acceptable_here = missing_col & missing_row & missing_region
        if not acceptable_here:
            raise Exception("Zero variants for empty cell")
        elif len(acceptable_here) == 1:
            (value, *rest) = acceptable_here
            candidates[i][j] = "{:^{}}".format("->{}<-".format(value), length)
            puzzle[i][j] = value
        elif len(acceptable_here) == 2:
            l_acc = list(acceptable_here)
            candidates[i][j] = "{:^{}}".format("[{},{}]".format(*l_acc), length)
    print_puzzle(candidates)
    return puzzle


def find_exclude_in_regions(puzzle, acceptable_values):
    """
    Finds only cell in the region that can contain given number
    """
    n_regions = 3
    region_indexes = [get_region_indexes(i, 3) for i in range(n_regions)]
    guesses = generate_empty_scratch()
    for region_i in range(n_regions):
        for region_j in range(n_regions):
            print("region {} {}".format(region_i,region_j))
            region_content = get_region(puzzle, region_i, region_j)
            missing_from_region = get_missing(set(region_content), acceptable_values)
            print("missing: ", missing_from_region)
            empty_cells = list(get_empty_cells_in_region(puzzle, acceptable_values,
                                                         region_indexes[region_i][0],
                                                         region_indexes[region_j][0],
                                                         region_indexes[region_i][1],
                                                         region_indexes[region_j][1]))

            for missing in missing_from_region:
                # проверяем, где может стоять эта цифра
                # todo: надо иметь фцию, которая проходит по массиву координат (как здесь empty_cells, но необязательно
                # регион, можно строку/столбец и проверяет, в каких местах может стоять каждая из отсутствующих цифр и
                # если остается 1 место -- то ставить

                # todo: так же иметь массив догадок -- где записаны пары мест, где могут стоять только 2 цифры :
                #   6 | [4, 3] |
                #     |        |
                #     | [4, 3] | 2
                # в таком случае в данном регионе остается только 5 мест, занятых цифрами 1, 5, 7, 8, 9
                pass


def solve(puzzle, acceptable_values):
    c_puzzle = copy.deepcopy(puzzle)
    rounds = 0
    while True:
        rounds += 1
        print("round #{}".format(rounds))
        new_puzzle = copy.deepcopy(c_puzzle)
        new_puzzle = find_single_missing(new_puzzle, acceptable_values)
        find_exclude_in_regions(new_puzzle, acceptable_values)
        # print(new_puzzle)
        if c_puzzle == new_puzzle:
            return new_puzzle
        c_puzzle = new_puzzle


if __name__ == "__main__":
    print("Puzzle:")
    print_puzzle(sample.hard["puzzle"])
    np = solve(sample.hard["puzzle"], sample.acceptable_values)
    print("Solved:")
    print_puzzle(np)
