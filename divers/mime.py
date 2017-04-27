import sys
import math

n = int(raw_input())  
q = int(raw_input())  
ext=[]
mt=[]
for i in xrange(n):
    x=raw_input().split()
    ext.insert(i,x[0].upper())
    if len(x)>1:
     mt.insert(i,x[1])
for i in xrange(q):
    fname = raw_input()  # One file name per line.
    l=fname.split('.')
    a=l[len(l)-1] 
    if '.' in fname and a.lower() in ext :
        print mt[ext.index(a.lower())]
    elif '.' in fname and a.upper()in ext :
            print mt[ext.index(a.upper())]
    else:
        print "UNKNOWN"
