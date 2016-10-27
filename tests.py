import unittest
import sample
import sudoku


class MyTestCase(unittest.TestCase):

    def test_column(self):

        col0 = sudoku.get_column(sample.sudoku, 0)
        self.assertEqual(col0, ['X', 'X', '8', '3', '4', 'X', '5', '2', 'X'])

    def test_row(self):

        row0 = sudoku.get_row(sample.sudoku, 0)

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
        reg0 = sudoku.get_region(sample.sudoku, 0, 0)
        self.assertEqual(reg0, ['X', 'X', 'X', 'X', 'X', '9', '8', '6', 'X'])

if __name__ == '__main__':
    unittest.main()
