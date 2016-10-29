import logging
import htmltable
from copy import deepcopy
import sample
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s')


def str_puzzle(puzzle):

    cell_horizontal_delim = "·"
    cell_intersection_delim = "·"
    cell_vertical_delim = "·"
    region_horizontal_delim = " | "
    region_intersection_delim = " + "
    region_vertical_delim = "-"

    strs = ["Graphical representation:"]
    fmt_row = region_horizontal_delim.join(["{}"]*3)
    fmt_interband_row = region_intersection_delim.join(["{}"]*3)
    for i in range(len(puzzle)):
        row = [x if x != "X" else " " for x in puzzle[i]]
        sub_row_fmt = cell_horizontal_delim.join(["{:^5}"] * 3)
        strs.append(fmt_row.format(sub_row_fmt.format(*row[0:3]),
                                   sub_row_fmt.format(*row[3:6]),
                                   sub_row_fmt.format(*row[6:9])))
        if i != len(puzzle)-1:
            if i % 3 == 2:
                sub = region_vertical_delim * 17
                strs.append(fmt_interband_row.format(sub, sub, sub))
            else:
                sub = cell_intersection_delim.join([cell_vertical_delim*5]*3)
                strs.append(fmt_row.format(sub, sub, sub))
    return "\n".join(strs)


class ZeroCandidatesException(Exception):
    def __init__(self, cell):
        self.cell = cell


class SudokuPuzzle:
    def __init__(self, puzzle, acceptable_values):
        self.puzzle = puzzle
        self.acceptable_values = acceptable_values
        self.size = len(puzzle)

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

    def __str__(self):
        return str_puzzle(self.puzzle)

    def __copy__(self):
        return self.__deepcopy__()

    def __deepcopy__(self, memodict={}):
        return SudokuPuzzle(
            deepcopy(self.puzzle),
            deepcopy(self.acceptable_values)
        )

    def __eq__(self, other):
        return self.puzzle == other.puzzle

    def is_finished(self):
        return len(list(self.get_empty_cells())) == 0

    def solve(self, silent=False, enable_desperate=True):
        c_puzzle = deepcopy(self)
        rounds = 0
        while True:
            if c_puzzle.is_finished():
                return c_puzzle
            rounds += 1
            if not silent:
                logging.info("{}\n\nround #{}".format("="*80,  rounds))
            new_puzzle = deepcopy(c_puzzle)
            if not silent:
                logging.info("Running strategy: find_single_missing")
            find_single_missing(new_puzzle, silent, draw_probable_values=False)
            if not silent:
                logging.info("Running strategy: find_exclude_in_regions")
            find_exclude_in_regions(new_puzzle, silent)
            if not silent:
                logging.info("Running strategy: find_exclude_in_columns")
            find_exclude_in_columns(new_puzzle, silent)
            if not silent:
                logging.info("Running strategy: find_exclude_in_rows")
            find_exclude_in_rows(new_puzzle, silent)
            if c_puzzle == new_puzzle:
                if enable_desperate:
                    if not silent:
                        logging.info("[despair mode]: Running strategy: nishio")
                    new_puzzle = nishio(new_puzzle, silent)
                    if c_puzzle == new_puzzle:
                        return new_puzzle
                else:
                    return new_puzzle
            c_puzzle = new_puzzle


def get_region_indexes(region_number, region_size):
    return region_number*region_size, (region_number+1)*region_size


def get_region_cells(reg_row, reg_column):
    row_section = get_region_indexes(reg_row, 3)
    col_section = get_region_indexes(reg_column, 3)
    cells = [(i, j) for i in range(*row_section) for j in range(*col_section)]
    return cells


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


def generate_scratch(sudoku, length, acceptable_values):
    return [["{:^{}}".format(sudoku.puzzle[i][j], length) if sudoku.puzzle[i][j] in acceptable_values else "     "
             for j in range(sudoku.size)] for i in range(sudoku.size)]


def get_possibles_for_cell(sudoku, i, j):
    missing_row = get_missing(set(sudoku.get_row(i)), sudoku.acceptable_values)
    missing_col = get_missing(set(sudoku.get_column(j)), sudoku.acceptable_values)
    missing_region = get_missing(set(sudoku.get_region_by_rc(i, j)), sudoku.acceptable_values)
    acceptable_here = missing_col & missing_row & missing_region
    return acceptable_here

########################################################################################################################
# methods
########################################################################################################################


def find_single_missing(sudoku, silent=False, draw_probable_values=True):
    """
    Finds all cells with only one variant
    """
    length = 5
    candidates_changed = False
    candidates = generate_scratch(sudoku, length, sudoku.acceptable_values)
    for cell in sudoku.get_empty_cells():
        i, j = cell
        acceptable_here = get_possibles_for_cell(sudoku, i, j)
        if not acceptable_here:
            raise ZeroCandidatesException(cell)
        elif len(acceptable_here) == 1:
            (value, *rest) = acceptable_here
            candidates[i][j] = "{:^{}}".format(" >{}< ".format(value), length)
            candidates_changed = True
            sudoku.puzzle[i][j] = value
        elif len(acceptable_here) == 2:
            # pass
            l_acc = list(acceptable_here)
            if draw_probable_values:
                candidates[i][j] = "{:^{}}".format("[{},{}]".format(*l_acc), length)
            candidates_changed = True
    if not silent:
        if candidates_changed:
            logging.info(str_puzzle(candidates))
        else:
            logging.info("<no changes>")


def exclude_cells_with_same_possible_values(sudoku, cells, missing_values, silent=False):
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

    if not silent:
        logging.debug("possible cells for values: {}".format(possible_values_cells))

    for k, v in possible_values_cells.items():
        if len(original_sets[k]) == len(possible_values_cells[k]) and len(original_sets[k]) != 1:
            # N equal sets of values were found in N cells
            # remove values from missing_values
            missing_values = missing_values.difference(original_sets[k])
            # remove cells from empty cells
            cells = [cell for cell in cells if cell not in v]

    if not silent:
        logging.debug("after stripping guesses: missing {} in cells {}".format(missing_values, cells))
    return cells, missing_values


def find_exclude_in_zone(sudoku, zone_cells, zone_description, silent=False):
    length = 5
    candidates_changed = False
    zone_content = [sudoku.puzzle[cell[0]][cell[1]] for cell in zone_cells ]
    candidates = generate_scratch(sudoku, length, sudoku.acceptable_values)
    missing_from_zone = get_missing(set(zone_content), sudoku.acceptable_values)
    if not missing_from_zone:
        return
    elif not silent:
        logging.debug("{}: missing: {}".format(zone_description, missing_from_zone))
    # find N cells with N variants where variants are equal between cells
    empty_cells = [cell for cell in zone_cells if sudoku.puzzle[cell[0]][cell[1]] not in sudoku.acceptable_values ]
    empty_cells, missing_from_zone = \
        exclude_cells_with_same_possible_values(sudoku,
                                                empty_cells,
                                                missing_from_zone,
                                                silent=silent)
    for missing_digit in missing_from_zone:
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
            candidates[i][j] = "{:^{}}".format(" >{}< ".format(missing_digit), length)
            candidates_changed = True
        if not silent:
            logging.debug("\t[{}] can be in: {}".format(missing_digit, possible_cells))
    for cell in empty_cells:
        i, j = cell
        possible_values = missing_from_zone & get_possibles_for_cell(sudoku, i, j)
        if len(possible_values) == 1:
            # цифра может быть только в 1 месте
            value = list(possible_values)[0]
            sudoku.puzzle[i][j] = value
            empty_cells = [e_cell for e_cell in empty_cells if e_cell != cell]
            candidates[i][j] = "{:^{}}".format(" >{}< ".format(value), length)
            candidates_changed = True


def find_exclude_in_columns(sudoku, silent=False):
    """
    in each column, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it
    :param sudoku: puzzle
    :param silent: don't log any messages
    :return:
    """
    length = 5
    candidates_changed = False
    candidates = generate_scratch(sudoku, length, sudoku.acceptable_values)
    for i_zone in range(sudoku.size):
        zone_description = "Column C{}".format(i_zone)
        zone_cells = [(i, i_zone) for i in range(sudoku.size)]
        find_exclude_in_zone(sudoku, zone_cells, zone_description, silent=False)
    if not silent:
        if candidates_changed:
            logging.info(str_puzzle(candidates))
        else:
            logging.info("<no changes>")


def find_exclude_in_rows(sudoku, silent=False):
    """
    in each row, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it
    :param sudoku: puzzle
    :param silent: don't log any messages
    :return:
    """
    length = 5
    candidates_changed = False
    candidates = generate_scratch(sudoku, length, sudoku.acceptable_values)
    for i_zone in range(sudoku.size):
        zone_description = "Row R{}".format(i_zone)
        zone_cells = [(i_zone, i) for i in range(sudoku.size)]
        find_exclude_in_zone(sudoku, zone_cells, zone_description, silent=False)
    if not silent:
        if candidates_changed:
            logging.info(str_puzzle(candidates))
        else:
            logging.info("<no changes>")


def find_exclude_in_regions(sudoku, silent=False):
    """
    in each region, for each missing digits, find cells where that digit can be. If there's only one
    possible cell -- fill it
    :param silent: don't log any messages
    :param sudoku:
    :return:
    """
    n_regions = 3
    length = 5
    candidates_changed = False
    candidates = generate_scratch(sudoku, length, sudoku.acceptable_values)
    for region_i in range(n_regions):
        for region_j in range(n_regions):
            zone_description = "Region {} {}".format(region_i, region_j)
            zone_cells = get_region_cells(region_i, region_j)
            find_exclude_in_zone(sudoku, zone_cells, zone_description, silent=False)
    if not silent:
        if candidates_changed:
            logging.info(str_puzzle(candidates))
        else:
            logging.info("<no changes>")


def nishio(sudoku, silent=False):
    for cell in sudoku.get_empty_cells():
        i, j = cell
        acceptable_here = get_possibles_for_cell(sudoku, i, j)
        if not acceptable_here:
            raise ZeroCandidatesException(cell)

        if not silent:
            logging.info("[!] Running hypothesis for cell {} (candidates {}).".format(cell, acceptable_here))
        possible_solutions = []
        for guess in acceptable_here:
            if not silent:
                logging.info("[*] Suppose cell {} is {}. Trying to solve or fail.".format(cell, guess))
            new_puzzle = deepcopy(sudoku.puzzle)
            new_puzzle[i][j] = guess
            guess_sudoku = SudokuPuzzle(new_puzzle, sudoku.acceptable_values)

            try:
                hypothesis_result = guess_sudoku.solve(silent=True, enable_desperate=False)
                if hypothesis_result.is_finished():
                    if not silent:
                        logging.info("[+] Hypothesis found solution, returning.")
                    return hypothesis_result
                else:
                    possible_solutions.append(hypothesis_result)
                    if not silent:
                        logging.info("[~] Hypothesis found PARTIAL solution, adding.")
            except ZeroCandidatesException as x:
                if not silent:
                    logging.info("[x] Hypothesis found contradiction at cell {}, continuing.".format(x.cell))
        if len(possible_solutions) == 1:
            return possible_solutions[0]


if __name__ == "__main__":
    hard = SudokuPuzzle(sample.medium["puzzle"], sample.acceptable_values)
    logging.warning("Puzzle:\n{}".format(hard))
    solved = hard.solve()
    logging.warning("="*80)
    logging.warning("\n\n\n\nSolved:\n{}".format(solved))
    htmltable.table(solved.puzzle)
