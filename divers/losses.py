import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
v=[int(i) for i in raw_input().split()]
x=v[0]
y=x
i=0
a=[]
r=0
if n>100:
    v.sort()
    r=v[0]-v[-2]
else:
    while i<len(v):
        j=0
        while j<i:
          if v[i]<v[j] and v[i]-v[j]<r:
              r=v[i]-v[j]
          j+=1    
        i+=1
if r>0:
    r=0
print r
