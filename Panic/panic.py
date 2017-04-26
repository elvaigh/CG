l={}
x,x,x,e,f,x,x,n=[int(i) for i in raw_input().split()]
for i in xrange(n):
 x=([int(j) for j in raw_input().split()])
 l[x[0]]=x[1]
while True:
 c,p,d=raw_input().split()
 c=int(c)
 p=int(p)
 if c!=e and c>=0 and((l[c]<p and d=="RIGHT")or(l[c]>p and d=="LEFT")):
  r="BLOCK"
 elif c==e and ((f>p  and d=="LEFT") or (f<p  and d=="RIGHT")) :
  r="BLOCK"
 else:
  r="WAIT"
 print r
