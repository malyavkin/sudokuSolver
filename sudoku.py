import copy
import sample


def print_puzzle(puzzle):
    delim = "|"
    for i in range(len(puzzle)):
        row = puzzle[i]
        print("{}   {}   {}".format(delim.join(row[0:3]), delim.join(row[3:6]), delim.join(row[6:9])))
        if i % 3 == 2:
            print()


class SudokuPuzzle:
    def __init__(self, puzzle, acceptable_values):
        self.puzzle = puzzle
        self.acceptable_values = acceptable_values
        self.guesses = [[[]  for j in range(9)] for i in range(9)]

    def get_row(self, row):
        """
        Returns contents of the row with current cell
        :param puzzle: sudoku, list of lists
        :param row: row number, 0-based
        :return: list of row contents
        """
        return list(self.puzzle[row])

    def get_column(self, column):
        """
        Returns contents of the column with current cell
        :param puzzle: sudoku, list of lists
        :param column: column number, 0-based
        :return: list of column contents
        """
        return [row[column] for row in self.puzzle]

    def get_region(self, reg_row, reg_column):
        row_section = get_region_indexes(reg_row, 3)
        col_section = get_region_indexes(reg_column, 3)
        region = [item for row in self.puzzle[slice(*row_section)] for item in row[slice(*col_section)]]
        return region

    def get_region_by_rc(self, row, column):
        row_section = get_section(row)
        col_section = get_section(column)
        region = [item for row in self.puzzle[slice(*row_section)] for item in row[slice(*col_section)]]
        return region

    def get_empty_cells(self):
        for i_row in range(len(self.puzzle)):
            for j_cell in range(len(self.puzzle[i_row])):
                if self.puzzle[i_row][j_cell] not in self.acceptable_values:
                    yield i_row, j_cell

    def get_empty_cells_in_region_by_region_ij(self, region_i, region_j):
        region_indexes = [get_region_indexes(i, 3) for i in range(3)]
        return self.get_empty_cells_in_region(region_indexes[region_i][0],
                                              region_indexes[region_j][0],
                                              region_indexes[region_i][1],
                                              region_indexes[region_j][1])

    def get_empty_cells_in_row(self, row_i):
        ijs = self.get_empty_cells()
        coords = lambda ij: ij[0] == row_i
        return filter(coords, ijs)

    def get_empty_cells_in_column(self, column_j):
        ijs = self.get_empty_cells()
        coords = lambda ij: ij[1] == column_j
        return filter(coords, ijs)

    def get_empty_cells_in_region(self, i_min, j_min, i_max, j_max):
        ijs = self.get_empty_cells()
        coords = lambda ij: i_min <= ij[0] < i_max and j_min <= ij[1] < j_max
        return filter(coords, ijs)

    def __str__(self):
        delim = "|"
        strs = []
        for i in range(len(self.puzzle)):
            row = [x if x !="X" else " " for x in self.puzzle[i]]
            subrow_fmt = "|".join(["{:^5}"]*3)
            strs.append("{}   {}   {}".format(subrow_fmt.format(*row[0:3]),
                                              subrow_fmt.format(*row[3:6]),
                                              subrow_fmt.format(*row[6:9])))
            if i % 3 == 2:
                strs.append("\n")
        return "\n".join(strs)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self, memodict={}):
        sp = SudokuPuzzle(
            copy.deepcopy(self.puzzle),
            copy.deepcopy(self.acceptable_values)
        )
        sp.guesses = copy.deepcopy(self.guesses)
        return sp

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def solve(self):
        c_puzzle = copy.deepcopy(self)
        rounds = 0
        while True:
            rounds += 1
            print("{}\n\nround #{}".format("="*80,  rounds))
            new_puzzle = copy.deepcopy(c_puzzle)
            find_single_missing(new_puzzle)
            find_exclude_in_regions(new_puzzle)
            find_exclude_in_columns(new_puzzle)
            find_exclude_in_rows(new_puzzle)
            # print(new_puzzle)
            if c_puzzle == new_puzzle:
                return new_puzzle
            c_puzzle = new_puzzle


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


def get_missing(lst: set, acceptable_values: set) -> set:
    """
    Returns list of values missing from list
    :return: list of values missing from list
    :rtype: set
    :param lst: said list
    :param acceptable_values: all acceptable values (usually digits 1-9)

    """
    return acceptable_values.difference(lst)


def generate_empty_scratch():
    return [[None for j in range(9)] for i in range(9)]


def generate_scratch(puzzle, length, acceptable_values):
    return [["{:^{}}".format(puzzle[i][j], length) if puzzle[i][j] in acceptable_values else "     "
             for j in range(9)] for i in range(9)]

def get_possibles_for_cell(sudoku, i, j):
    missing_row = get_missing(set(sudoku.get_row(i)), sudoku.acceptable_values)
    missing_col = get_missing(set(sudoku.get_column(j)), sudoku.acceptable_values)
    missing_region = get_missing(set(sudoku.get_region_by_rc(i, j)), sudoku.acceptable_values)
    acceptable_here = missing_col & missing_row & missing_region
    return acceptable_here

########################################################################################################################
# methods
########################################################################################################################


def find_single_missing(sudoku):
    """
    Finds all cells with only one variant
    """
    length = 5
    candidates = generate_scratch(sudoku.puzzle, length, sudoku.acceptable_values)
    for i, j in sudoku.get_empty_cells():
        acceptable_here = get_possibles_for_cell(sudoku, i, j)
        if not acceptable_here:
            raise Exception("Zero variants for empty cell")
        elif len(acceptable_here) == 1:
            (value, *rest) = acceptable_here
            candidates[i][j] = "{:^{}}".format("->{}<-".format(value), length)
            sudoku.puzzle[i][j] = value
        elif len(acceptable_here) == 2:
            # pass
            l_acc = list(acceptable_here)
            candidates[i][j] = "{:^{}}".format("[{},{}]".format(*l_acc), length)
    print_puzzle(candidates)


def exclude_cells_with_same_possible_values(sudoku, cells, missing_values):
    possible_values_cells = {}
    original_sets = {}
    cells = list(cells)
    for cell in cells:
        i, j = cell
        possible_values = get_possibles_for_cell(sudoku, i, j)
        pv_hash = "_".join(sorted(list(possible_values)))
        if pv_hash not in possible_values_cells:
            possible_values_cells[pv_hash] = []
            original_sets[pv_hash] = possible_values
        possible_values_cells[pv_hash].append(cell)

    print(possible_values_cells)

    for k, v in possible_values_cells.items():
        if len(original_sets[k]) == len(possible_values_cells[k]):
            # N equal sets of values were found in N cells
            # remove values from missing_values
            missing_values = missing_values.difference(original_sets[k])
            # remove cells from empty cells
            cells = [cell for cell in cells if cell not in v]

    print("after stripping guesses: missing {} in cells {}".format(missing_values, cells))
    return cells, missing_values

def find_exclude_in_columns(sudoku):
    """
    in each column, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it
    :param sudoku:
    :return:
    """
    n_columns = 9
    length = 5
    candidates = generate_scratch(sudoku.puzzle, length, sudoku.acceptable_values)
    for j_column in range(n_columns):
        print("column {}".format(j_column))
        column_content = sudoku.get_column(j_column)
        missing_from_column = get_missing(set(column_content), sudoku.acceptable_values)
        print("\tmissing: ", missing_from_column)
        # find N cells with N variants where variants are equal between cells
        empty_cells = sudoku.get_empty_cells_in_column(j_column)
        empty_cells, missing_from_column = \
            exclude_cells_with_same_possible_values(sudoku,
                                                    empty_cells,
                                                    missing_from_column)
        for missing_digit in missing_from_column:
            possible_cells = []

            for cell in empty_cells:
                i, j = cell
                if missing_digit in get_possibles_for_cell(sudoku, i, j):
                    possible_cells.append(cell)
            if len(possible_cells) == 1:
                i, j = possible_cells[0]
                # цифра может быть только в 1 месте
                sudoku.puzzle[i][j] = missing_digit
                empty_cells = [cell for cell in empty_cells if cell != possible_cells[0]]
                candidates[i][j] = "{:^{}}".format("->{}<-".format(missing_digit), length)
            print("\t[{}] can be in: {}".format(missing_digit, possible_cells))
        for cell in empty_cells:
            i, j = cell
            possible_values = missing_from_column & get_possibles_for_cell(sudoku, i, j)
            if len(possible_values) == 1:
                # цифра может быть только в 1 месте
                value = list(possible_values)[0]
                sudoku.puzzle[i][j] = value
                empty_cells = [e_cell for e_cell in empty_cells if e_cell != cell]
                candidates[i][j] = "{:^{}}".format("->{}<-".format(value), length)
    print_puzzle(candidates)


def find_exclude_in_rows(sudoku):
    """
    in each row, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it

    :param sudoku:
    :return:
    """
    n_rows = 9
    length = 5
    candidates = generate_scratch(sudoku.puzzle, length, sudoku.acceptable_values)
    for i_row in range(n_rows):
        print("row {}".format(i_row))
        row_content = sudoku.get_row(i_row)
        missing_from_row = get_missing(set(row_content), sudoku.acceptable_values)
        print("\tmissing: ", missing_from_row)
        # find N cells with N variants where variants are equal between cells
        empty_cells = sudoku.get_empty_cells_in_row(i_row)
        empty_cells, missing_from_row = \
            exclude_cells_with_same_possible_values(sudoku,
                                                    empty_cells,
                                                    missing_from_row)
        for missing_digit in missing_from_row:
            possible_cells = []

            for cell in empty_cells:
                i, j = cell
                if missing_digit in get_possibles_for_cell(sudoku, i, j):
                    possible_cells.append(cell)
            if len(possible_cells) == 1:
                i, j = possible_cells[0]
                # цифра может быть только в 1 месте
                sudoku.puzzle[i][j] = missing_digit
                empty_cells = [cell for cell in empty_cells if cell != possible_cells[0]]
                candidates[i][j] = "{:^{}}".format("->{}<-".format(missing_digit), length)
            print("\t[{}] can be in: {}".format(missing_digit, possible_cells))
        for cell in empty_cells:
            i, j = cell
            possible_values = missing_from_row & get_possibles_for_cell(sudoku, i, j)
            if len(possible_values) == 1:
                # цифра может быть только в 1 месте
                value = list(possible_values)[0]
                sudoku.puzzle[i][j] = value
                empty_cells = [e_cell for e_cell in empty_cells if e_cell != cell]
                candidates[i][j] = "{:^{}}".format("->{}<-".format(value), length)
    print_puzzle(candidates)


def find_exclude_in_regions(sudoku):
    """
    in each region, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it

    :param sudoku:
    :return:
    """
    n_regions = 3
    length = 5
    candidates = generate_scratch(sudoku.puzzle, length, sudoku.acceptable_values)
    for region_i in range(n_regions):
        for region_j in range(n_regions):
            print("region {} {}".format(region_i, region_j))
            region_content = sudoku.get_region(region_i, region_j)
            missing_from_region = get_missing(set(region_content), sudoku.acceptable_values)
            print("\tmissing: ", missing_from_region)
            # find N cells with N variants where variants are equal between cells
            empty_cells = sudoku.get_empty_cells_in_region_by_region_ij(region_i, region_j)
            empty_cells, missing_from_region = \
                exclude_cells_with_same_possible_values(sudoku,
                                                        empty_cells,
                                                        missing_from_region)

            for missing_digit in missing_from_region:
                possible_cells = []

                for cell in empty_cells:
                    i, j = cell
                    if missing_digit in get_possibles_for_cell(sudoku, i, j):
                        possible_cells.append(cell)
                if len(possible_cells) == 1:
                    i, j = possible_cells[0]
                    # цифра может быть только в 1 месте
                    sudoku.puzzle[i][j] = missing_digit
                    empty_cells = [cell for cell in empty_cells if cell != possible_cells[0]]
                    candidates[i][j] = "{:^{}}".format("->{}<-".format(missing_digit), length)
                print("\t[{}] can be in: {}".format(missing_digit, possible_cells))
            for cell in empty_cells:
                i, j = cell
                possible_values = missing_from_region & get_possibles_for_cell(sudoku, i, j)
                if len(possible_values) == 1:
                    # цифра может быть только в 1 месте
                    value = list(possible_values)[0]
                    sudoku.puzzle[i][j] = value
                    empty_cells = [e_cell for e_cell in empty_cells if e_cell != cell]
                    candidates[i][j] = "{:^{}}".format("->{}<-".format(value), length)

                # todo: так же иметь массив догадок -- где записаны пары мест, где могут стоять только 2 цифры :
                #   6 | [4, 3] |
                #     |        |
                #     | [4, 3] | 2
                # в таком случае в данном регионе остается только 5 мест, занятых цифрами 1, 5, 7, 8, 9
    print_puzzle(candidates)



if __name__ == "__main__":
    hard = SudokuPuzzle(sample.hard["puzzle"], sample.acceptable_values)
    print("Puzzle:\n{}".format(hard))
    solved = hard.solve()
    print("="*80, "\nSolved:\n{}".format(solved))

