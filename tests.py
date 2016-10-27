import unittest
import sample, solve

class MyTestCase(unittest.TestCase):

    def test_column(self):
        sudoku = solve.SudokuPuzzle(sample.sudoku)
        col0 = sudoku.get_column(0)
        self.assertEqual(col0, ['X', 'X', '8', '3', '4', 'X', '5', '2', 'X'])

    def test_row(self):
        sudoku = solve.SudokuPuzzle(sample.sudoku)
        row0 = sudoku.get_row(0)

        self.assertEqual(row0, list("XXXX6824X"))

    def test_section(self):
        self.assertEqual(solve.get_section(0), (0,3))
        self.assertEqual(solve.get_section(1), (0,3))
        self.assertEqual(solve.get_section(2), (0,3))

        self.assertEqual(solve.get_section(3), (3, 6))
        self.assertEqual(solve.get_section(4), (3, 6))
        self.assertEqual(solve.get_section(5), (3, 6))

        self.assertEqual(solve.get_section(6), (6, 9))
        self.assertEqual(solve.get_section(7), (6, 9))
        self.assertEqual(solve.get_section(8), (6, 9))

    def test_regions(self):
        sudoku = solve.SudokuPuzzle(sample.sudoku)
        reg0 = sudoku.get_region(0, 0)
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
