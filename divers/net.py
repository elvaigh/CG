import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
xs=[]
ys=[]
def d(y,ys):
    s=0
    for i in ys:
            s+=abs(y-i)
    return s
    
for i in xrange(n):
    x, y = [int(j) for j in raw_input().split()]
    xs.extend([x])
    ys.extend([y])
a=max(xs)-min(xs)
s=0
t=[]
ys.sort()
print >> sys.stderr, "Debug messages...",len(ys)
i=0
j=max(ys)+min(ys)/2
j=0
x=min(d(1,ys),d(0,ys))
for i in range(len(ys)):
    if j<100:
        t.extend([d(ys[i],ys)])
        j+=1
    else:
        i=len(ys)
x=min(x,min(t))
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
print >> sys.stderr, "Debug messages...",s,a
if len(ys)>1:
    print a+x
else:
    print  a

