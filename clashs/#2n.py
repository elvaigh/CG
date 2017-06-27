import sys
import math

n = int(input())

print(n*"#")
for i in range(n):print(' '*(n-1-i)+'#'*(2*i+1))
for i in range(n):print(' '*i+'#'*(2*(n-1-i)+1))