import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

start, n = [long(i) for i in raw_input().split()]

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
last=''
turn=0
def next(b):
    l=0
    bits=bin(b)[2:]
    for i in str(bits):
        if i=='1':
            l+=3
        else:
            l+=4
    return l
def S(n,start):
    global turn
    global last
    i=0
    x=0
    while i<n and last!=start:
        x=next(start)
        last=start
        turn+=1
        start=x
        i+=1
    return x
print S(n,start)
