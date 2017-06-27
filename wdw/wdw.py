# To debug: print("Debug messages...", file=sys.stderr)
import sys
import math
import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
#ha=hash(tuple([k,i]))
size = int(input())
units_per_player = int(input())

def valide(x, y):
    return (x < size and x > -1 and y < size and y > -1)
def value(c):
    if c=='.':return -1
    return int(c)
class Case(object):
    def __init__(self,x,y):self.x,self.y=x,y
    def dist2(c,self):return (self.x-c.x)**2+(self.y-c.y)**2
    def dist(c,self):return math.sqrt(self.dist2(c))
    def getKey(self):return hash(tuple([self.x,self.y]))
    def getNeighbour(self,ddr):
        global g
        if    ddr=="N" and valide(self.x,self.y-1):return g[Case(self.x,self.y-1).getKey()]
        elif  ddr=="NE" and valide(self.x+1,self.y-1):return g[Case(self.x+1,self.y-1).getKey()]
        elif  ddr=="E" and valide(self.x+1,self.y):return g[Case(self.x+1,self.y).getKey()]
        elif  ddr=="SE" and valide(self.x+1,self.y+1):return g[Case(self.x+1,self.y+1).getKey()]
        elif  ddr=="S" and valide(self.x,self.y+1):return g[Case(self.x,self.y+1).getKey()]
        elif  ddr=="SW" and valide(self.x-1,self.y+1):return g[Case(self.x-1,self.y+1).getKey()]
        elif  ddr=="W" and valide(self.x-1,self.y):return g[Case(self.x-1,self.y).getKey()]
        elif  ddr=="NW" and valide(self.x-1,self.y-1):return g[Case(self.x-1,self.y-1).getKey()]
    def getNeighbours(self):
        dirs=["N","NE","E","SE","S","SW","W","NW"]
        nighbours=[]
        me=g[Case(self.x,self.y).getKey()]
        #print("me ",me, file=sys.stderr)
        for i in dirs:
            neighbour=self.getNeighbour(i)
            if neighbour and neighbour[1]>-1 and neighbour[1]<4 and (me[1]>=neighbour[1] or me[1]==neighbour[1]-1 ) :nighbours+=[neighbour]
        return nighbours
unitsPos=[]
unitsOther=[]
for i in range(units_per_player):
    unitsPos+=[Case(0,0)]
    unitsOther+=[Case(0,0)]
g={}
def applly(action):
    type, index, dir_1, dir_2=action
    unitPos=unitsPos[int(index)]
    targetd=unitPos.getNeighbour(dir_1)
    targetb=unitPos.getNeighbour(dir_2)
    if type=="MOVE&BUILD" and targetd and targetb:
         g[targetb[0].getKey()]=[targetb[0],targetb[1]+1]
         unitsPos[int(index)]=targetd[0]
    elif targetd and targetb:
        g[unitPos.getKey()]=[unitPos,g[unitPos.getKey()][1]+1]
        unitsPos[int(index)]=targetb[0]

def scor():
    i,s=0,0
    while i<units_per_player:
        myng=unitsPos[i].getNeighbours()
        hisng=unitsOther[i].getNeighbours()
        for m in myng:
            if (m[1]<=g[unitsPos[i].getKey()][1] or m[1]==g[unitsPos[i].getKey()][1]-1):
                if  m[1]==3:s+=100
                else:s+=1 
        # for o in hisng:
        #     if (o[1]<=g[unitsOther[i].getKey()][1] or m[1]==g[unitsOther[i].getKey()][1]-1):
        #         if  m[1]==3:s+=-100
        #         else:s+=-1 
        i+=1
    return s+len(myng)
def countNeighbours(ll):
    i,s=0,0
    while i<units_per_player:
      s+=len(ll[i].getNeighbours())
      i+=1
    return s
        
# game loop
while True:
    move="ACCEPT-DEFEAT Well done!"
    moves=[]
    for i in range(size):
        row = input()
        for j in  range(size):
            g[hash(tuple([j,i]))]=[Case(j,i),value(row[j])]
    for i in range(units_per_player):
        unit_x, unit_y = [int(j) for j in input().split()]
        unitsPos[i]=Case(unit_x, unit_y)
        
    for i in range(units_per_player):
        other_x, other_y = [int(j) for j in input().split()]
        unitsOther[i]=Case(other_x, other_y)
    legal_actions = int(input())
    h=0
    for i in range(legal_actions):
        type, index, dir_1, dir_2 = input().split()
        unitPos=unitsPos[int(index)]
        gg=g.copy()
        unitsPosC=unitsPos.copy()
        unitsOtherc=unitsOther.copy()
        action=[type, index, dir_1, dir_2]
        applly(action)
        s=scor()
        if s>h:h=s;move=' '.join(action)
        g=gg
        unitsPos=unitsPosC
        unitsOther=unitsOtherc
        # target=unitPos.getNeighbour(dir_1)
        # ngbrs=unitPos.getNeighbours()
        # if  target[1]+len(ngbrs)>h:h=len(ngbrs)+target[1];move=' '.join([type, index, dir_1, dir_2])
    print("neibghours ",h,countNeighbours(unitsOther), file=sys.stderr)
    print(move)