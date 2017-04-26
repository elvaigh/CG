input()
o=0
m=900
for j in list(map(int,input().split())):
 k=abs(j)
 if k<m or(k==m and j>0):m,o=k,j 
print(o)
