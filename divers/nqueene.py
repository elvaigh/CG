import sys
import math

n = int(input())

class NQueen:
    # @return a list of lists of string
    def solveNQueens(self, n):
        self.__ans = []
        self.__stack = []
        self.__n = n
        self.solve(0)
        return self.__ans
        
        
    def solve(self, depth):
        if depth == self.__n:
            self.__ans.append(self.answer2board(self.__stack))
        else:
            for i in range(self.__n):
                if self.isSafe(i):
                    self.__stack.append(i)
                    self.solve(depth + 1)
                    self.__stack.pop()
                    
    def isSafe(self, pos):
        idx = len(self.__stack)
        for i in range(idx):
            if self.__stack[i] == pos or abs(idx - i) == abs(pos - self.__stack[i]):
                return False
        return True
        
    def answer2board(self, ans):
        ret = []
        for i in range(len(ans)):
            ret.append('.' * ans[i] + 'Q' + '.' * (self.__n - ans[i] - 1))
        return ret
print(len(NQueen().solveNQueens(n)))
