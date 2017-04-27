import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l=raw_input()
x=list(map(int,l[1:len(l)-1].split(',')))
x.sort()
r=[]
k=0
j=0
while k<len(x):
 if j==0:
    i=x[k]
 if k<len(x) -1 and x[k+1]==x[k]+1:
    j=x[k]+1
 else:
    if j==0:
        r.extend([str(i)])
    else:
        if j-i>1:
            r.extend([str(i)+'-'+str(j)])
        else:
            r.extend([str(i)])
            r.extend([str(i+1)])
        j=0
 k+=1
s=''
for i in r:
    if r.index(i)!=len(r)-1:
        s+=i+','
    else:
        s+=i
print s
