
n = int(raw_input())
if n==1:
 print '.*\n* *'
else:
 l=1
 j=2*n-1
 for i in range(n):
     s=''
     if i==0:
      s+='.'
      for k in range(j-1):
        s+=' '
     else:
      for k in range(j):
        s+=' '
     for k in range(l):
        s+='*'
     print s
     l+=2
     j-=1
l=1
j=n-1
m=2*n-1
for i in range(n):
     s=''
     for k in range(j):
        s+=' '
     for k in range(l):
        s+='*'
     for k in range(m):
        s+=' '
     for k in range(l):
        s+='*'
     print s
     l+=2
     m-=2
     j-=1
