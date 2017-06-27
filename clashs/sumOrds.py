s=input().upper()
print(chr(sum(map(ord,s))//len(s)))