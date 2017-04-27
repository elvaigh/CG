import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

r = [int(raw_input())]
l = int(raw_input())

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
j=1
m=0
n=0
while j<l:
    j+=1
    m=0
    y=r[m]
    x=[]
    while m<len(r):
        k=0
        n=m
        while n<len(r) and r[n]==y:
         #r.remove(r[m])
         n+=1
         k+=1
        x.extend([k,y])
        if n<len(r):
            y=r[n]
            m+=k
        else:
            m=len(r)
    r=x
for i in r:
    print i,
