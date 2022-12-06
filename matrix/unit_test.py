import unittest
import random
from mul import *


class TestMatrixMultiplication(unittest.TestCase):
    def test_matrix_multiplication(self):
        n = 2
        random.seed(1234)
        matmul = MatrixMultiplication(n)
        res = matmul.standard_matrix_product()
        create_mat(n)
        # open the file
        with open("matrix.out") as f:
            lines = f.read().splitlines()

        self.A = []
        self.B = []
        self.matrix = self.A
        for line in lines:
            if line != "":
                self.matrix.append([int(el) for el in line.split("\t")])
            else:
                self.matrix = self.B

        C = [[0 for i in xrange(n)] for j in xrange(n)]
        for i in xrange(n):
            for j in xrange(n):
                for k in xrange(n):
                    C[i][j] += self.A[i][k] * self.B[k][j]
        self.assertEqual(res, C)


if __name__ == "__main__":
    unittest.main()
