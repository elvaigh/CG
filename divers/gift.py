import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


def knapSack(totalWeight, objects):
	currentWeight = 0
	subSet = []
	for counter in xrange(len(objects)):
		if currentWeight + objects[counter][-1] <= totalWeight:
			currentWeight += objects[counter][-1]
			subSet.append(objects[counter])
        return subSet

n = int(raw_input())
c = int(raw_input())
s=0
b=[]
j=1
q=0
for i in xrange(n):
    a=int(raw_input())
    if(a==q):
        j+=1
    q=a
    s+=a
    b.insert(i,a)
b.sort()
print >> sys.stderr, "Debug messages...",c/n
e=int(c/n)
if s<c:
    print "IMPOSSIBLE"
elif j==n:
    for i in range(n-1):
        print c/n
    if c%n==0:
        print c/n
    else:
        print 1+c/n
else:
    s=[]
    i=0
    k=0
    while b[i]<=e:
         s.extend([b[i]])
         c-=b[i]
         i+=1
         k+=1
    j=i
    while c>0:
       if n-j==1:
           s.extend([c])
           c=0
       elif n-j==2:
           if c%2==0:
               s.extend([c/2])
               s.extend([c/2])
               c=0
           else:
                s.extend([c/2])
                s.extend([1+c/2])
                c=0
       else:
           e=c/(n-i)
           if b[i]<=e:
               c-=b[i]
               s.extend([b[i]])
           else:
               s.extend([e])
               c-=e
           i+=1
           
    for i in s:
            print i
                
