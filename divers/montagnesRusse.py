
# To debug: print >> sys.stderr, "Debug messages..."
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, c, n = [int(i) for i in raw_input().split()]
p=[]
for i in xrange(n):
   p+=[int(raw_input())]
j=0
ss=0
sss=sum(p)
#print >> sys.stderr, "Debug messages...",p
if l>sss:ss=sss*c
else:
    for i in range(c):
       s=0
       j=j%len(p)
       while s+p[j]<=l:
           s+=p[j];j+=1;j=j%len(p)
       ss+=s
print ss
