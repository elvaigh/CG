import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

w, h, my_id = [int(i) for i in input().split()]
k=0
l=[]
def save(l,x,y):
   i,j=x,y
   while i<len(l) and i>=0:
        while j<len(l[0]) and l[i][j]=='.':
            j+=1
        if abs(j-y)<3:
            while j>=0 and l[i][j]=='.':
                j-=1
        if abs(j-y)>=4:
            return i,j
        else:
            if i<len(l):
                i+=1
            else:
                if i==len(l):
                    i=x
                else:
                    i-=1
   return -1,-1 
# game loop
k=0
def chaine(s):
    x=s[0].count('.')==len(s[0])
    j=0
    for i in range(len(s)):
        if s[i][0]=='.':
            j+=1
    return j==len(s) 
while True:
    s=[]
    for i in range(h):
        s.append(input())
    entities = int(input())
    for i in range(entities):
        entity_type, owner, x, y, param_1, param_2 = [int(j) for j in input().split()]
        if entity_type==0 and my_id==owner:
            a,b=x,y
            x0,y0=a,b
            print("Debug messages...",a,b,file=sys.stderr)
            
    
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)
    print("MOVE",x0,y0)
