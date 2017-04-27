import sys
import math
import string

n = int(raw_input())
w=[]
for i in xrange(n):
    w.append(raw_input())
l= raw_input()

def score(s):
    v=0
    for i in s:
        if i in "aeionrtsu":v+=1
        elif i in "dg":v+=2
        elif i in "bcmp":v+=3
        elif i in "fhvwy":v+=4
        elif i=='k':v+=5
        elif i in "jx":v+=8
        else:v+=10
    return v


def simple(a,l):
    for i in a:
        if a.count(i)>l.count(i):return False
    return True
def subOf(a,b):
    for i in a:
        if i not in b:return False
    return True
s,m=0,''
k=0
for i in w:
    if simple(i,l) and subOf(i,l):
        tt=score(i)
        #print >> sys.stderr, "Debug messages...",i,tt
        if tt>s:m,s=i,tt
print m
