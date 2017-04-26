a,b,c,d=map(int,input().split())
while 1:
 if b>d:x="S"
 if a<c:x="W"
 if a>c and b>d:x="SE"
 if a<c and b>d:x="SW"
 print(x)
 x='E';d+=1
