import sys
import math
X=[]
Y=[]
P=[]
for i in range(30):
    for j in range(20):
        P.append([i,j])
def present( x, y):
    if x<0 or x>29 or y<0 or y>19:
        return 1
    else:
        if [x,y] in X or [x,y] in Y:
            return 1
    return 0;

def decouper(xi,yi):
    a,b,c,d=0,0,0,0
    for i in P:
        if i not in Y and i not in X:
            if present(xi-1, yi)==0 and i[0]<xi:
                a+=1
            elif present(xi+1, yi)==0  and i[0]>xi:
                b+=1
            elif present(xi, yi-1)==0 and i[1]<yi:
                c+=1
            elif present(xi, yi+1)==0 and i[1]>yi:
                d+=1
    if max(a,b,c,d)==a:
        print('LEFT')
    elif max(a,b,c,d)==b:
        print('RIGHT')
    elif max(a,b,c,d)==c:
        print('UP')
    elif max(a,b,c,d)==d:
        print('DOWN')
    else:
        jouer(xi,yi)

def jouer(xi,yi):
    if present(xi+1,yi)==0:
            print("RIGHT")
    elif present(xi-1,yi)==0:
            print("LEFT")
    elif present(xi,yi-1)==0:
            print("UP")
    elif present(xi,yi+1)==0:
            print("DOWN")
j=0
while True:
    n, p = [int(i) for i in input().split()]
    xi,yi=0,0
    for i in range(n):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if i==p:
            X.append([x1,y1])
            xi,yi=x1,y1
        else:
            Y.append([x1,y1])
    decouper(xi,yi)
