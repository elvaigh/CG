import sys
import math

n = int(input())  # the number of relationships of influence
g={}
for i in range(n):
    # x: a relationship of influence between two people (x influences y)
    x, y = [int(j) for j in input().split()]
    if x in g.keys():g[x].extend([y])
    else:g[x]=[y]
a=list(g.keys())
b=list(g.values())
tmp=[]
for i in b:tmp.extend(i)
b=list(set(tmp))
k=0

x=[]
for i in b:
    if i in a:x.extend([i])
print(len(x)+2)
