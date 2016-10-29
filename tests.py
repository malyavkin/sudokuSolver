import unittest
import sample
import sudoku


class MyTestCase(unittest.TestCase):

    def test_column(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        col0 = easy.get_column(0)
        self.assertEqual(col0, ['X', 'X', '8', '3', '4', 'X', '5', '2', 'X'])

    def test_row(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        row0 = easy.get_row(0)

        self.assertEqual(row0, list("XXXX6824X"))

    def test_section(self):
        self.assertEqual(sudoku.get_section(0), (0, 3))
        self.assertEqual(sudoku.get_section(1), (0, 3))
        self.assertEqual(sudoku.get_section(2), (0, 3))

        self.assertEqual(sudoku.get_section(3), (3, 6))
        self.assertEqual(sudoku.get_section(4), (3, 6))
        self.assertEqual(sudoku.get_section(5), (3, 6))

        self.assertEqual(sudoku.get_section(6), (6, 9))
        self.assertEqual(sudoku.get_section(7), (6, 9))
        self.assertEqual(sudoku.get_section(8), (6, 9))

    def test_regions(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        reg0 = easy.get_region_by_rc(0, 0)
        self.assertEqual(reg0, ['X', 'X', 'X', 'X', 'X', '9', '8', '6', 'X'])

    def test_missing(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        col0 = set(easy.get_column(0))
        self.assertEqual(sudoku.get_missing(col0, sample.acceptable_values), {'1', '6', '9', '7'})

    def test_yielding_empty_cells(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        for i, j in easy.get_empty_cells():
            self.assertEqual(sample.easy["puzzle"][i][j], "X")

    def test_get_empty_cells_in_region(self):
        easy = sudoku.SudokuPuzzle(sample.easy["puzzle"], sample.acceptable_values)
        em = list(easy.get_empty_cells_in_region(0, 0, 3, 3))
        self.assertEqual(len(em), 6)

    def test_get_region_cells(self):
        cells = sudoku.get_region_cells(0, 0)
        self.assertIn((0, 0), cells)
        self.assertIn((2, 2), cells)
        self.assertNotIn((2, 3), cells)


class StrategyTestCase(unittest.TestCase):
    def test_locked_candidates(self):
        puzzle = [
              ["8", "X", "9",    "1", "2", "X",    "X", "X", "X"],
              ["X", "X", "X",    "3", "4", "X",    "X", "5", "X"],
              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],

              ["X", "X", "X",    "X", "X", "5",    "X", "X", "X"],
              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],
              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],

              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],
              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],
              ["X", "X", "X",    "X", "X", "X",    "X", "X", "X"],
        ]
        su = sudoku.SudokuPuzzle(puzzle, sample.acceptable_values)
        solved = su.solve(enable_desperate=False)
        self.assertEqual(solved.puzzle[0][1], "5")

    def test_sole_candidate(self):
        puzzle = [
            ["X", "X", "X", "X", "X", "1", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "6", "X", "X", "X"],

            ["X", "X", "X", "4", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "8", "X", "X", "X", "X"],
            ["2", "X", "9", "X", "X", "X", "X", "X", "7"],

            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "3", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
        ]
        su = sudoku.SudokuPuzzle(puzzle, sample.acceptable_values)
        solved = su.solve(enable_desperate=False)
        self.assertEqual(solved.puzzle[5][5], "5")

    def test_unique_candidate(self):
        puzzle = [
            ["X", "X", "4", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],

            ["X", "4", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],

            ["5", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "4", "X", "X", "X"],
        ]
        su = sudoku.SudokuPuzzle(puzzle, sample.acceptable_values)
        solved = su.solve(enable_desperate=False)
        self.assertEqual(solved.puzzle[7][0], "4")

    def test_block_row_interaction(self):
        puzzle = [
            ["5", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "5", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "5"],

            ["X", "X", "X", "1", "X", "2", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "3", "X", "4", "X", "5", "X"],

            ["X", "X", "X", "X", "X", "X", "5", "X", "X"],
            ["X", "X", "X", "X", "X", "5", "X", "X", "X"],
            ["X", "X", "5", "X", "X", "X", "X", "X", "X"],
        ]
        su = sudoku.SudokuPuzzle(puzzle, sample.acceptable_values)
        solved = su.solve(enable_desperate=False)
        self.assertEqual(solved.puzzle[4][3], "5")

    def test_block_block_interaction(self):
        puzzle = [
            ["X", "X", "X", "X", "X", "X", "8", "X", "X"],
            ["X", "X", "8", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "8", "X", "X", "X", "X", "X"],

            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["1", "2", "X", "X", "3", "4", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],

            ["X", "X", "X", "X", "X", "X", "X", "X", "8"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
            ["X", "X", "X", "X", "X", "X", "X", "X", "X"],
        ]
        su = sudoku.SudokuPuzzle(puzzle, sample.acceptable_values)
        solved = su.solve(enable_desperate=False)
        self.assertEqual(solved.puzzle[4][7], "8")


if __name__ == '__main__':
    unittest.main()
