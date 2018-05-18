import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

s = "".join(input().split())

col = int(input())
j=0
t=""
g=0
for  i in range(len(s)):
    if col*(i+1)<len(s):print(s[col*i:(i+1)*col])
    else:break
print(s[(i)*col:len(s)])
