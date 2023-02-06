from create_mat import create_mat
import time

try:
    xrange
except NameError:
    xrange = range


class MatrixMultiplication:

    def print_matrix(self, mat):
        for line in mat:
            print("\t".join(map(str, line)))

    def standard_matrix_product(self):
        start = time.time()
        n = len(self.A)
        C = [[0 for i in xrange(n)] for j in xrange(n)]
        for i in xrange(n):
            for j in xrange(n):
                for k in xrange(n):
                    C[i][j] += self.A[i][k] * self.B[k][j]
        print("Remote Time: %f" % ((time.time() - start)*1000), "ms")
        return C


if __name__ == "__main__":
    dim = int(input("Enter the dimension of the matrix: "))
    mat = MatrixMultiplication(dim)

    C = mat.standard_matrix_product()
    mat.print_matrix(C)
