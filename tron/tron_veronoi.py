import sys
import math
import random
import copy
# To debug: print("Debug messages...", file=sys.stderr)
line=[]
players=[]
sx,sy=0,0
w,h=30,20
def jouer(ox,oy,nx,ny):
    if ox<nx:print("RIGHT");return
    if oy>ny:print("UP");return
    if ox>nx:print("LEFT");return
    print("DOWN")
def valide(x,y):return x<w and x>0 and y<h and y>0
def dist2(x,y,a,b):return (x-a)**2+(y-b)**2
def dist(x,y,a,b):return math.sqrt(dist2(x,y,a,b))

def veronoi(start,s):
    tmp=[]
    for i in range(w):
        for j in range(h):
            inside=True
            for k in s:
                if dist2(i,j,k[0],k[1])>dist2(start[0],start[1],k[0],k[1]):inside=False;break
            if inside:tmp+=[[i,j]]
    return tmp
def free(i):
    for j in range(len(players)):
        if i in players[j]:return False
    return True
def others(p):
    tmp=[]
    for j in range(len(players)):
        if j!=p and [-1,-1] not in players[j]:tmp+= players[j]
    return tmp
def voisins(start):
    moves=[]
    if valide(start[0]-1,start[1]):moves+=[[start[0]-1,start[1]]]
    if valide(start[0],start[1]-1):moves+=[[start[0],start[1]-1]]
    if valide(start[0]+1,start[1]):moves+=[[start[0]+1,start[1]]]
    if valide(start[0],start[1]+1):moves+=[[start[0],start[1]+1]]
    return moves
def bestMove(p):
    tmp=None
    start=players[p][0]
    # oo=others(p)
    # vv0=veronoi(start,oo) 
   
    moves=voisins(start)
    for i in moves:
        cp=copy.copy(players[p])
        players[p]+=i
        # oo=others(p)
        # vv=veronoi(players[p][0],oo) 
        if len(players[p])>len(cp):tmp=i
        players[p]=cp
    if tmp==None:tmp=moves[0]
    return tmp
g=[[0 for i in range(w)]for j in range(h)]
j=0
while True:
    n, p = [int(i) for i in input().split()]
    if j==0:
        players=[[] for i in range(n)];j+=1
    for i in range(n):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        if [x0,y0] not in players[i]:players[i]+=[[x0,y0]]
        if j>0:players[i]+=[[x1,y1]]
    start=players[p][0]
    tt=bestMove(p)
    jouer(start[0],start[1],tt[0],tt[1])
    #print("UP")
    print("Debug messages...",tt, file=sys.stderr)
