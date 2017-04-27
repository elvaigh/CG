import sys
import math

def repartir(x,i,j):
    if i>0:x[i-1][j]+=1
    if i+1<len(x):x[i+1][j]+=1
    if j>0:x[i][j-1]+=1
    if j+1<len(x):x[i][j+1]+=1
    x[i][j]-=4
def normal(x):
    for i in x:
        for  j in i:
            if j>3 :return False
    return True
def equilibre(x,n):
    for i in range(n):
        for  j in range(n):
            if x[i][j]>3 :repartir(x,i,j)
n = int(input())
x=[]
y=[]
for j in range(n):
    tmp=[]
    for i in input():tmp.extend([int(i)])
    x.append(tmp)
for j in range(n):
    k=0
    for i in input():
        x[j][k]+=int(i)
        k+=1
while(not normal(x)):equilibre(x,n)
for i in x:
    s=''
    for j in i:s+=str(j)
    print(s)
