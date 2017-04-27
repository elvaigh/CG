import sys
import math

x={}

l, h = [int(i) for i in input().split()]
s=list()

for i in range(20):
    s.extend([''])
for i in range(h):
    n= input()
    j=0
    k=0
    while j<20:
      s[j]+=n[(j)*l:(j+1)*l]
      if i<h-1:
         s[j]+='\n'
      j+=1
k=0
for i in s:
    x[i]=k
    k+=1
s1 = int(input())
n1=''
k=1
a1=0
j=1
for i in range(s1):
    n1+= input()
    if k%l!=0:
        n1+='\n'
    if k%l==0:
      a1+=x[n1]*20**(int((s1)/l)-j)
      j+=1
      n1=''
    k+=1
s2 = int(input())
a2=0
j=1
n1=''
for i in range(s2):
    n1+= input()
    if k%l!=0:
        n1+='\n'
    if k%l==0:
      a2+=x[n1]*20**(int((s2)/l)-j)
      j+=1
      n1=''
    k+=1
o = input()
# print("a1",a1)
# print("a2",a2)
if o=='+':
    s=int(a1)+int(a2)
elif o=='-':
    s=int(a1)-int(a2)
elif o=='*':
    s=int(a1)*int(a2)
else:
    s=int(a1)/int(a2)
    
def base(n):
    x=[]
    if n==0:
         x=['0']
    while n!=0:
     s=str(n%20)
     x.extend([s])
     n=int(n/20)
    return x
    
a=base(int(s))[::-1]
for i in a:
    for j in x:
        if str(x[j])==i:
            print(j)
