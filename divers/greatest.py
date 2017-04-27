import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(raw_input())
c=[]
p=False
n=False
for i in raw_input().split(' '):
    if i!='.' and i!='-':
     c.extend([int(i)])
    elif i=='.':
         p=True
    else:
        n=True
s=''
if n:
    s='-'
    c.sort()
    if p:
        for i in range(len(c)):
            if i==1:
                s+='.'+str(c[i])
            else:
                s+=str(c[i])
    else:
        for i in range(len(c)):
            s+=str(c[i])
else:
    c.sort(reverse=True)
    if p:
        for i in range(len(c)):
            if i==len(c)-1 and c[i]!=0:
                s+='.'+str(c[i])
            else:
                s+=str(c[i])
        if c[i]==0:
            s=s[:len(s)-1]
    else:
        for i in range(len(c)):
            s+=str(c[i])
if sum(c)==0:
 s=0   
print(s)
