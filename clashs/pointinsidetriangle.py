import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def sign (p1x,p1y, p2x,p2y, p3x,p3y):
    return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)
    
def  PointInTriangle ( ptx,pty, v1x,v1y,  v2x,v2y, v3x,v3y):
  
    b1 = sign(ptx,pty, v1x,v1y, v2x,v2y) < 0
    b2 = sign(ptx,pty, v2x,v2y, v3x,v3y) < 0
    b3 = sign(ptx,pty, v3x,v3y, v1x,v1y) < 0.
    return ((b1 == b2) and (b2 == b3))
x, y = [int(i) for i in input().split()]
n = int(input())
for i in range(n):
    x_1, y_1, x_2, y_2, x_3, y_3 = [int(j) for j in input().split()]
    if(PointInTriangle(x,y,x_1, y_1, x_2, y_2, x_3, y_3)):
        print("inside")
    else:print("outside")
