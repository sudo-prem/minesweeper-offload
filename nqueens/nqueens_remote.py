
class NQueens:
    def __init__(self, N):
        self.N = N
        self.board = [[0]*self.N for _ in range(self.N)]
        self.n = N
    
    def is_attack(self,i, j):
    #checking if there is a queen in row or column
        for k in range(0,self.N):
            if self.board[i][k]==1 or self.board[k][j]==1:
                return True
        #checking diagonals
        for k in range(0,self.N):
            for l in range(0,self.N):
                if (k+l==i+j) or (k-l==i-j):
                    if self.board[k][l]==1:
                        return True
        return False

    def solve(self,n):
        if n==0:
            return True
        for i in range(0,self.N):
            for j in range(0,self.N):
                '''checking if we can place a queen here or not
                queen will not be placed if the place is being attacked
                or already occupied'''
                if (not(self.is_attack(i,j))) and (self.board[i][j]!=1):
                    self.board[i][j] = 1
                    #recursion
                    #wether we can put the next queen with this arrangement or not
                    if self.solve(n-1)==True:
                        return True
                    self.board[i][j] = 0

        return False
        
    def print_solution(self):
        for i in self.board:
            print (i)

    
#Number of queens
# print ("Enter the number of queens")
# N = int(input())



if __name__ == "__main__":
    N=6
    nqueens = NQueens(N)
    nqueens.solve(N)
    nqueens.print_solution()
