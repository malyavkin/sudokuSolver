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
        self.assertEqual(sudoku.get_section(0), (0,3))
        self.assertEqual(sudoku.get_section(1), (0,3))
        self.assertEqual(sudoku.get_section(2), (0,3))

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


if __name__ == '__main__':
    unittest.main()
