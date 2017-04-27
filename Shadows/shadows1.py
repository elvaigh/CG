import sys
import math



w, h = [int(i) for i in raw_input().split()]
n = int(raw_input())  # maximum number of turns before game over.
x0, y0 = [int(i) for i in raw_input().split()]
p=0
j=0
n0=n
xmax,ymax=w,h
xmin,ymin=0,0
# game loop
while True:
    bomb_dir = raw_input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    x,y=x0,y0
    
    if bomb_dir=='U' :
        xmin=max(x0-1,0)
        xmax=min(x0+1,w)
        ymax=y0
        y0-=max(1,int((ymax-ymin)/2))
    elif bomb_dir=='UR' :
        ymax=y0
        y0-=max(1,int((ymax-ymin)/2))
        xmin=x0
        x0+=max(1,int((xmax-xmin)/2))
    elif bomb_dir=='UL':
        print >> sys.stderr, "ull",xmax-xmin,ymax-ymin,
        ymax=y0
        xmax=x0
        if n0==7 :
            y0=max(n-1,int((ymax-ymin)/2))
            x0=max(n-1,int((xmax-xmin)/2))
        else:
            y0-=max(1,int((ymax-ymin)/2))
            x0-=max(1,int((xmax-xmin)/2))
    elif bomb_dir=='D' :
        xmin=max(x0-1,0)
        xmax=min(x0+1,w)
        ymin=y0
        y0+=max(1,int((ymax-ymin)/2))
    elif bomb_dir=='DR' :
        ymin=y0
        xmin=x0
        x0+=max(1,int((xmax-xmin)/2))
        y0+=max(1,int((ymax-ymin)/2))
    elif bomb_dir=='DL' :
        ymin=y0
        xmax=x0
        x0-=max(1,int((xmax-xmin)/2))
        y0+=max(1,int((ymax-ymin)/2))
    elif bomb_dir=='R' :
        ymax=min(h,y0+1)
        ymin=max(y0-1,0)
        xmin=x0
        x0+=max(1,int((xmax-xmin)/2))
    elif bomb_dir=='L':
        ymax=min(h,y0+1)
        ymin=max(0,y0-1)
        xmax=x0
        x0-=max(1,int((xmax-xmin)/2))
    print >> sys.stderr, "ebug messages...",xmax,ymax,xmin,ymin
    # the location of the next window Batman should jump to.
    n-=1
    print int(x0),int(y0)
