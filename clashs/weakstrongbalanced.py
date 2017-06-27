import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def isp(n):
 return not any(n%a==0 for a in range(2,int(math.sqrt(n)+1)))

def nextp(n):
 m=n+1
 while not isp(m):
  m+=1
 return m
 
def prevp(n):
 m=n-1
 while not isp(m):
  m-=1
 return m

n = int(input())

av = (nextp(n)+prevp(n))//2

print('BALANCED' if av == n else 'WEAK' if n < av else 'STRONG')
