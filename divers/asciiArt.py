import sys
import os
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def lol(v,x,l):
    y=''
    if v.lower()=='a':
        for i in x :
             y+=i[0:l]
             y+='\n'
    elif v.lower()=='b':
        for i in x :
             y+=i[l:2*l]   
             y+='\n'
    elif v.lower()=='c':
        for i in x :
              y+=i[2*l:3*l]
              y+='\n'
    elif v.lower()=='d':
        for i in x :
              y+=i[3*l:4*l]
              y+='\n'
    elif v.lower()=='e':
        for i in x :
            y+=i[4*l:5*l]
            y+='\n'
    elif v.lower()=='f':
        for i in x :
              y+=i[5*l:6*l]
              y+='\n'
    elif v.lower()=='g':
        for i in x :
              y+=i[6*l:7*l]
              y+='\n'
    if v.lower()=='h':
        for i in x :
              y+=i[7*l:8*l]
              y+='\n'
    elif v.lower()=='i':
        for i in x :
             y+=i[8*l:9*l]   
             y+='\n'
    elif v.lower()=='j':
        for i in x :
              y+=i[9*l:10*l]
              y+='\n'
    elif v.lower()=='k':
        for i in x :
              y+=i[10*l:11*l]
              y+='\n'
    elif v.lower()=='l':
        for i in x :
             y+=i[11*l:12*l]
             y+='\n'
    elif v.lower()=='m':
        for i in x :
             y+=i[12*l:13*l]
             y+='\n'
    elif v.lower()=='n':
        for i in x :
              y+=i[13*l:14*l]
              y+='\n'
    if v.lower()=='o':
        for i in x :
             y+=i[14*l:15*l]
             y+='\n'
    elif v.lower()=='p':
        for i in x :
              y+=i[15*l:16*l]  
              y+='\n'
    elif v.lower()=='q':
        for i in x :
              y+=i[16*l:17*l]
              y+='\n'
    elif v.lower()=='r':
        for i in x :
              y+=i[17*l:18*l]
              y+='\n'
    elif v.lower()=='s':
        for i in x :
              y+=i[18*l:19*l]
              y+='\n'
    elif v.lower()=='t':
        for i in x :
             y+=i[19*l:20*l]
             y+='\n'
    elif v.lower()=='u':
        for i in x :
              y+=i[20*l:21*l]
              y+='\n'
    if v.lower()=='v':
        for i in x :
              y+=i[21*l:22*l]
              y+='\n'
    elif v.lower()=='w':
        for i in x :
            y+=i[22*l:23*l]  
            y+='\n'
    elif v.lower()=='x':
        for i in x :
              y+=i[23*l:24*l]
              y+='\n'
    elif v.lower()=='y':
        for i in x :
               y+=i[24*l:25*l]
               y+='\n'
    elif v.lower()=='z':
        for i in x :
              y+=i[25*l:26*l]
              y+='\n'
    else:
        for i in x :
                y+=i[26*l:27*l]
                y+='\n'
               
    return y
            
l = int(raw_input())
h = int(raw_input())
t = raw_input()
x=[]
for i in xrange(h):
    row=raw_input()
    x.insert(i,row)
j=0
s=''
f=[]
for i in t :  
 f.insert(j,lol(i,x,l).split('\n'))
 j+=1

for i in range(h):
   j=0
   while j<len(f):
    s+=f[j][i]
    j+=1
   s+='\n'
print s  

# To debug: print >> sys.stderr, "Debug messages..."

