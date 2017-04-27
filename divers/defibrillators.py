import sys
import math
import numpy as np
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
def dist(x1,y1,x2,y2):
    x=(x2-x1)*(math.cos((y1+y2)/2))
    y=y2-y1
    return math.sqrt(x*x+y*y)*6371
lon = raw_input()
lat = raw_input()
n = int(raw_input())
d=[]
for i in xrange(n):
    defib = raw_input()
    d.insert(i,defib.split(";"))
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
da=dist(float(lon.replace(',','.')),float(lat.replace(',','.')),float(d[0][4].replace(',','.')),float(d[0][5].replace(',','.')))
m=d[0]
for x in d:
    j=dist(float(lon.replace(',','.')),float(lat.replace(',','.')),float(x[4].replace(',','.')),float(x[5].replace(',','.')))
    if da>j:
         m=x
         da=j
print m[1]

