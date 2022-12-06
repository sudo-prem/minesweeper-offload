import unittest
import random
from nqueens import *


class TestNQueens(unittest.TestCase):
    def test_nqueens(self):
        for i in range(1, 10):
            n = i
            random.seed(1234)
            nqueens = NQueens(n)
            nqueens.solve(n)

            another_one = NQueens(n)
            another_one.solve(n)
            self.assertEqual(nqueens.print_solution(),
                             another_one.print_solution())


if __name__ == "__main__":
    unittest.main()
