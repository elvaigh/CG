import sys
import math

# Don't let the machines win. You are humanity's last hope...

width = int(raw_input())  # the number of cells on the X axis
height = int(raw_input())  # the number of cells on the Y axis
x=[]
y=[]
for i in xrange(height):
    line = raw_input()  # width characters, each either 0 or .
    for k in range(len(line)) :
       x.insert(k,line[k])
    y.insert(i,x)
    x=[]
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."
a=len(y)
b=len(y[0])
print >> sys.stderr, "Debug messages...",y,a,b
# Three coordinates: a node, its right neighbor, its bottom neighbor
for i in range(a):
    for j in range(b):
        if(y[i][j]=='0' and i<a and j<b):
            k=j+1
            l=i+1
            while k<b and y[i][k]!='0':
                k+=1
            while l<a and y[l][j]!='0':
                l+=1    
            if(k<b and l<a):
                print j,' ',i,' ',k,' ',i,' ',j,' ',l
            elif(k<b):
                print j,' ',i,' ',k,' ',i,' -1 -1'
            elif(l<a):
                print j,' ',i,' -1 -1 ',' ',j,l
            else:
                print j,' ',i,' -1 -1 -1 -1'
        elif y[i][j]!='.':
            print j,' ',i,' -1 -1 -1 -1'
       
