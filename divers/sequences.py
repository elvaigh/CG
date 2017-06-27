import sys,math

n=int(input())
seq=[]
def allin(s):
	for i in seq:
		if i not in s:return False
	return True

for i in range(n):
	s=input()
	seq+=[s]
tmp=""
i=0
while not allin(tmp):
	
	k=0
	while seq[i] not in tmp:tmp+=seq[i][k];k+=1
	print(tmp)
	i+=1
	#if i>=len(seq):break
print("HHHH",tmp)
