import sys
import math
import string
l=' '+string.ascii_uppercase
# To debug: print >> sys.stderr, "Debug messages..len(s)"
start=' '
def next(e,start,end=True):
    s=''
    x=l.index(e)
    y=l.index(start)
    n=min(abs(y-x)+1,(abs(y-x)+28)%27)
    if e>start:
        for i in range(n):
            s+='+'
    else:
        for i in range(n):
            s+='-'
    s+="."
    if end:
        s+='>'
    return s
p = raw_input()

s=""
n=len(p)
if p.count(p[0])==n:
    if l.index(start)+l.index(p[0])<len(l)-l.index(p[0]):x='+'*(l.index(p[0])-l.index(start))
    else:x='-'*(len(l)-l.index(p[0]))
    s=x+'.'*(n)
else:
    for i in p:
        if l.index(start)<l.index(i):
            s+='+'*(l.index(i)-l.index(start))+'.'
        else:s+='-'*(l.index(start)-l.index(i))+'.'
        start=i
        print >> sys.stderr, "Debug messages...",len(s),i,start
print >> sys.stderr, "Debug messages...",p
print s
