import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
x=[]
i=0
a={}
k=0
n = int(raw_input())
for i in xrange(n):
    s=raw_input()
    s.replace(' ','')
    x.append(s)
    a[x[i]]=i
nb_orders = int(raw_input())

for i in xrange(nb_orders):
    o = raw_input()
    if 'after' in o:
      o=o.split(' after ')
      p,q=o[0],o[1]
      s=''
      for i in p:
          if i!=' ':s+=i
      p=s
      s=''
      for i in p:
          if i!=' ':s+=i
      p=s
      a[p]=a[q]+1
      
    else:
      o=o.split(' before ')
      p,q=o[0],o[1]
      a[q]=a[p]+1

j=1
while j<=len(a.keys()):
    for  i in a.keys():
        if a[i]==j:print i
    j+=1
        
        
