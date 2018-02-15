import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

note_types = input()
n = int(input())

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
factor=list(map(int,note_types.split()))
def moneyback(amount, coins):
    n = len(coins)
    chosen = [0] * n 
    for i in range(n - 1, -1, -1):
        while amount >= coins[i]: 
            amount -= coins[i] 
            chosen[i] += 1 
    assert amount == 0 
    return chosen

    
x=moneyback(n,factor)
s=""
for i in range(len(x)):
    if x[i]!=0:s=str(x[i])+"x"+str(factor[i])+" "+s
print(s[:-1])
