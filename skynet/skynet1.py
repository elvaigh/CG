import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways

n, l, e = [int(i) for i in raw_input().split()]
print >> sys.stderr, "Debug messages...",l
x=[]
for i in xrange(l):
    # n1: N1 and N2 defines a link between these nodes
   x.insert(i,[int(j) for j in raw_input().split()])
w=[]
for i in xrange(e):
    e = int(raw_input())  # the index of a gateway node
    w.insert(i,e)
# game loop
a=[]
b=[]
f=True
k=8
d=0
while True:
    si = int(raw_input()) 
    
    for i in x:
      for j in w:
        if f and si in i and j in i and i not in b:
            a=i
            print >> sys.stderr, "Debug messages...kkk",i
            f=False
    if f:
     if d!=0:
      for i in x:
        if f  and i not in b and si in i:
            a=i
            f=False
            print >> sys.stderr, "Debug messages...bbb",b
     else:
      if(len(x)>75):
        while x[k] in b and k<75:
            k+=1
        if k<75:
            a=x[k]
        else:
            a=x[4]
        print >> sys.stderr, 'iniiiiiiiiiiiiiiiiiiiiiiiiiiiiii',a
      else:
         a=x[0]
      d+=1
    print a[0],a[1]
    b.append(a)
    f=True
    print >> sys.stderr, "cccc..",si,w,b
    # To debug: print >> sys.stderr, "Debug messages..."
