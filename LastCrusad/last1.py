import sys
import math

# To debug: print >> sys.stderr, "Debug messages..."
w, h = [int(i) for i in raw_input().split()]

c={}
cc={}
for i in range(h):
    l=list(map(int,raw_input().split()))
    for k in range(len(l)):
        ha=hash(tuple([k,i]))
        cc[ha]=[i,k]
        c[ha]=l[k]

ex = int(raw_input())  
while True:
    xi, yi, pos = raw_input().split()
    x,y=int(xi),int(yi)
    ha=hash(tuple([x,y]))
    t=c[ha]
    print >> sys.stderr,x,y,t,"Debug messages..."
    if t==1:y+=1
    
    elif t==2 or t==6:
        if pos=='RIGHT':x-=1
        else:x+=1
    elif t==3:y+=1
    elif t==4:
        if pos=='RIGHT':y+=1
        else:x-=1
    elif t==5:
        if pos=='LEFT':y+=1
        else:x+=1
    elif t==7 or t==8 or t==9:y+=1
    elif t==10:x-=1
    elif t==11:x+=1
    elif t==12 or t==13:y+=1
    
    print x,y
