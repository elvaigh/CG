import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def pgcd(a,b):
     if b==0:
        return a
     else:
        r=a%b
        return pgcd(b,r)

n = int(raw_input())
for i in xrange(n):
    x,y = map(int ,raw_input().split('/'))
    if y==0:
        print 'DIVISION BY ZERO'
    elif x%y==0:
        print x/y
    else:
        print >> sys.stderr, "Debug messages...",x,y
        a=abs(x)/abs(y)
        if x<0 and y>0 or x>0 and y<0 :
            a=-a
        print >> sys.stderr, "Debug messages...",a
        if a!=0:
          b=pgcd(x-a*y,y)
          s=str(a)+' '+str((abs(x-a*y))/abs(b))+'/'+str(abs(y)/abs(b))
        else:
            b=pgcd(x,y)
            print >> sys.stderr, "Debug messages...",b
            s=str(x/b)+'/'+str(y/b)
        print s
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

