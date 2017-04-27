mport sys
import math

n = int(raw_input())
x=[]
for i in xrange(n):
    x.insert(i,int(raw_input()))
k=abs(x[0]-x[1])
x.sort()
i=1
while i< len(x)-1:
        i+=1
        if abs(x[i]-x[i-1])<k:
            k=abs(x[i]-x[i-1])
print k
