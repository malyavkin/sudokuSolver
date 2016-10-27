import unittest
import sample
import sudoku



class MyTestCase(unittest.TestCase):

    def test_column(self):

        col0 = sudoku.get_column(sample.easy["puzzle"], 0)
        self.assertEqual(col0, ['X', 'X', '8', '3', '4', 'X', '5', '2', 'X'])

    def test_row(self):

        row0 = sudoku.get_row(sample.easy["puzzle"], 0)

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
        reg0 = sudoku.get_region_by_rc(sample.easy["puzzle"], 0, 0)
        self.assertEqual(reg0, ['X', 'X', 'X', 'X', 'X', '9', '8', '6', 'X'])

    def test_missing(self):
        col0 = set(sudoku.get_column(sample.easy["puzzle"], 0))
        self.assertEqual(sudoku.get_missing(col0, sample.acceptable_values), {'1', '6', '9', '7'})

    def test_yielding_empty_cells(self):
        for i, j in sudoku.get_empty_cells(sample.easy["puzzle"], sample.acceptable_values):
            self.assertEqual(sample.easy["puzzle"][i][j], "X")

    def test_get_empty_cells_in_region(self):
        em = list(sudoku.get_empty_cells_in_region(sample.easy["puzzle"], sample.acceptable_values,
                                                   0, 0, 3, 3))
        self.assertEqual(len(em), 6)



if __name__ == '__main__':
    unittest.main()
