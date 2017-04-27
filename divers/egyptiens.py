import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

a, b = [int(i) for i in raw_input().split()]

if a==0 or b==0:
    print str(b)+' * '+str(a)+'\n= 0'
else:
    
    c=min(a,b)
    k=1
    l=max(a,b)
    m=l
    x=''
    print str(l)+' * '+str(c)
    while c!=0:
        if c%2!=0:
          c-=1
          x+=' + '+str(l)
          print('= '+str(l)+' * '+str(c)+x)
        else:
            l*=2
            c=int(c/2)
            print('= '+str(l)+' * '+str(c)+x)
    print '= '+str(a*b)
