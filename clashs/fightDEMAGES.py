import math as m
a,b=map(int,input().split())
c,d=map(int,input().split())
if d==0 or a/d>c/b:x,y=1,c/b 
else:x,y=2,a/d
print(x,m.ceil(y))