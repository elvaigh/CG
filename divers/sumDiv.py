s=0
n=int(input())
for i in range(1,n+1):
     if i<=n//2:s+=(n//i)*i
     else:s+=i
print(s)
