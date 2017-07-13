# To debug: print >> sys.stderr, "Debug messages..."
import sys
import math

l, c, n = [int(i) for i in raw_input().split()]
p=[]
sss=0
ss=0
k=0
s=0
j=0
for i in xrange(n):
   p+=[int(raw_input())]
   if s+p[j]<=l:s+=p[j];j+=1
   else:ss+=s;s=0;k+=1
   sss+=p[-1]
j=j%n
if l>sss:ss=sss*c
else:
    for i in range(c-k):
       while s+p[j]<=l:
           s+=p[j];j+=1;j=j%n
       ss+=s
       s=0
print ss