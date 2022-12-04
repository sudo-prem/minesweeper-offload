import psutil
import os
import time


class CodeSync:
    def __init__(self,n,board,N,retVal=None):
        self.n = n
        self.board = board
        self.N = N
        self.retVal = retVal
       

    # Getters
    def get_n(self):
        return self.n
    def get_board(self):
        return self.board
    def get_N(self):
        return self.N
    
    # Setters
    def set_n(self, n):
        self.n = n
    def set_board(self, board):
        self.board = board
    def set_N(self, N):
        self.N = N

    
