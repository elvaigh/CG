import sys
import math

def to_int(s):
    
   a=0
   if s=='J':
      a=11
   elif s=='Q':
      a=12
   elif s=='K':
       a=13
   elif s=='A':
       a=14
   else:
       a=int(s)
       if a==1:
           a=10
   return a
            
n = int(raw_input())  # the number of cards for player 1
c1=[]
c2=[]
for i in xrange(n):
    c1.insert(i,to_int(raw_input()[0])) # the n cards of player 1
   
m = int(raw_input())  # the number of cards for player 2
for i in xrange(m):
    c2.insert(i,to_int(raw_input()[0])) # the m cards of player 2

# Write an action using print
# To debug: print >> sys.stdrr, "Debug messages..."
b=''
q=[]
p=[]
s=0
game=True
while len(c1)>=1 and len(c2)>=1 and game:
    x=c1[0]
    y=c2[0]
    c1.remove(x)
    c2.remove(y)
    print >> sys.stderr, "Debug messages...",x,y,len(c1),len(c2)
    if x==y:
        if len(c1)>3 and len(c2)>3:
            p.extend([x])
            p.extend(c1[:3])
            p1=c1[:3]
            for w in p1:
                if w in c1:
                    c1.remove(w)
            q.extend([y])
            q.extend(c2[:3])
            q1=c2[:3]
            for w in q1:
                if w in c2:
                    c2.remove(w)
        else:
            game=False
            s-=1
    elif x-y>0:
            if len(p)>0:
                c1.extend(p)
                c1.extend([x])
                c1.extend(q)
                c1.extend([y])
                p=[]
                q=[]
            else:
                 c1.extend([x])
                 c1.extend([y])
            s+=1
    elif x-y<0:
            if len(p)>0:
                c2.extend(p)
                c2.extend([x])
                c2.extend(q)
                c2.extend([y])
                p=[]
                q=[]
            else:
                c2.extend([x])
                c2.extend([y])
            s+=1
if len(c2)>0 and len(c1)==0:
        print 2,s
if len(c1)>0 and len(c2)==0:
        print 1,s
if len(c1)>0 and len(c2)>0:
    print 'PAT'
