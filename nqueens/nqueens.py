
import sys
sys.path.append('../offload')
from offmat import offmat


already_called_recursively = False


class NQueens:
    def __init__(self, N):
        self.N = N
        self.board = [[0]*self.N for _ in range(self.N)]
        self.n = N

    def is_attack(self, i, j):
        #checking if there is a queen in row or column
        for k in range(0, self.N):
            if self.board[i][k] == 1 or self.board[k][j] == 1:
                return True
        #checking diagonals
        for k in range(0, self.N):
            for l in range(0, self.N):
                if (k+l == i+j) or (k-l == i-j):
                    if self.board[k][l] == 1:
                        return True
        return False

    def solve(self, n):
        # code_sync_obj = CodeSync(n,self.board,self.N)
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

        codeSyncDict['functionName'] = 'solve'

        codeForIC = codeSyncDict

        codeForIC['saved_args'] = saved_args
        codeForIC['dict'] = numberOfParamsInSelf

        task = self.solve
        # offMatResult = offmat(task, code_sync_obj)
        offMatResult = offmat(task, codeSyncDict, codeForIC)
        # offMatResult = False
        if offMatResult == False:
            #if n is 0, solution found
            if n == 0:
                return True
            for i in range(0, self.N):
                for j in range(0, self.N):
                    '''checking if we can place a queen here or not
                    queen will not be placed if the place is being attacked
                    or already occupied'''
                    if (not (self.is_attack(i, j))) and (self.board[i][j] != 1):
                        self.board[i][j] = 1
                        #recursion
                        #wether we can put the next queen with this arrangement or not
                        if self.solve(n-1) == True:
                            return True
                        self.board[i][j] = 0

            return False
        else:
            self.board = offMatResult['board']
            if (offMatResult['retVal'] == True):
                return True
            return False

    def print_solution(self):
        for i in self.board:
            print(i)


#Number of queens
# print ("Enter the number of queens")
# N = int(input())


if __name__ == "__main__":
    N = int(input("Enter number of queens: "))
    nqueens = NQueens(N)
    nqueens.solve(N)
    nqueens.print_solution()
