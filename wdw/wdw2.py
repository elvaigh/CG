# To debug: print("Debug messages...", file=sys.stderr)
import sys
import math
import random
from collections import namedtuple

size = int(input())
units_per_player = int(input())
Action=namedtuple('Action',['type','index','move','build','to_height','from_height','move_from','move_to','build_at','command'])
def getNieghbor(pos,direction):
    x,y=pos[0],pos[1]
    if 'N' in direction:y-=1
    elif 'S' in direction:y+=1
    if 'W' in direction:x-=1
    elif 'E' in direction:x+=1
    return (x,y)

def getHeight(pos,grid):return int(grid[pos[1]][pos[0]])

def dist(posa,posb):return max(abs(posa[0]-posb[0]),abs(posa[1]-posb[1]))
def evaluate_move(action,grid,enemies):
    help_enemy=0
    buildOn3=0
    blockE=0
    build_height=getHeight(action.build_at,grid)
    for  e in enemies:
        enemy_height=getHeight(e,grid)
        d=dist(e,action.build_at)
        if enemy_height>=2 and d==1 and build_height==2:help_enemy=1
        if enemy_height>=2 and d==1 and build_height==3:blockE=1
    if build_height==3:buildOn3=1

    return (-help_enemy,blockE,action.to_height,-buildOn3,build_height)
def evaluate(action,grid,enemies):
    if action.type=="MOVE&BUILD":return evaluate_move(action,grid,enemies)
    return evaluate_push(action,grid,enemies)
def evaluate_push(action,grid,enemies):
    return (-1,-1,-1,-1,-1)
# game loop
while True:
    move="ACCEPT-DEFEAT Well done!"
    grid=[]
    myUnits=[]
    otherUnits=[]
    for i in range(size):grid.append(input())

    for i in range(units_per_player):
        unit_x, unit_y = [int(j) for j in input().split()]
        myUnits.append((unit_x, unit_y ))
      

    for i in range(units_per_player):
        other_x, other_y = [int(j) for j in input().split()]
        otherUnits.append((other_x, other_y))
       
    legal_actions = int(input())
    actions=[]
    for i in range(legal_actions):
        command=input()
        atype, index, dir_1, dir_2 = command.split()
        index=int(index)
        move_from=myUnits[index]
        move_to=getNieghbor(move_from,dir_1)
        build_at=getNieghbor(move_to,dir_2)
        to_height=getHeight(move_to,grid)
        from_height=getHeight(move_from,grid)
        a=Action(atype,index,dir_1,dir_2,to_height,from_height,move_from,move_to,build_at,command)
        actions.append(a)
    best=max(actions,key=lambda a: evaluate(a,grid,otherUnits))
    print(best.command)