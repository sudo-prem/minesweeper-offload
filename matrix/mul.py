from offmat import offmat
from create_mat import create_mat
import time
import sys
import random
import unittest
sys.path.append('../offload')

try:
    xrange
except NameError:
    xrange = range


class MatrixMultiplication:
    def __init__(self, ndim):
        create_mat(ndim)
        self.ndim = ndim
        self.filename = "matrix.out"
        lines = []
        with open(self.filename) as f:
            lines = f.read().splitlines()
        self.A = []
        self.B = []
        self.matrix = self.A
        for line in lines:
            if line != "":
                self.matrix.append([int(el) for el in line.split("\t")])
            else:
                self.matrix = self.B

    def print_matrix(self, mat):
        for line in mat:
            print("\t".join(map(str, line)))

    def standard_matrix_product(self):
        n = len(self.A)
        saved_args = locals()
        codeSyncDict = {}
        numberOfParamsInSelf = 0

        for key, val in saved_args.items():
            if key == 'self':
                for i in val.__dict__:
                    codeSyncDict[i] = val.__dict__[i]
                    numberOfParamsInSelf += 1
            else:
                codeSyncDict[key] = val

        codeSyncDict['functionName'] = 'standard_matrix_product'

        codeForIC = codeSyncDict

        codeForIC['saved_args'] = saved_args
        codeForIC['dict'] = numberOfParamsInSelf

        task = self.standard_matrix_product

        offMatResult = offmat(task, codeSyncDict, codeForIC)
        # offMatResult = False
        if offMatResult == False:
            start = time.time()
            C = [[0 for i in xrange(n)] for j in xrange(n)]
            for i in xrange(n):
                for j in xrange(n):
                    for k in xrange(n):
                        C[i][j] += self.A[i][k] * self.B[k][j]

            print("Local Time: %f" % (time.time() - start), "sec")
            print("**************************\n")
            return C
        else:
            return offMatResult['retVal']


if __name__ == "__main__":
    inp = [line.strip() for line in open("matrix.in")]
    s = inp[0].split(' ')
    dimensions = []

    for c in s:
        if c.isdigit():
            dimensions.append(int(c))

    for dim in dimensions:
        matmul = MatrixMultiplication(int(dim))
        res = matmul.standard_matrix_product()

        for line in res:
            print("\t".join(map(str, line)))
        print()
