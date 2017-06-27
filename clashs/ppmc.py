import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

def ppcm(l):
    if len(l) == 2:
        return l[0] * l[1] // math.gcd(l[0], l[1]);
    else:
        return ppcm([l[0]] + [ppcm(l[1:])])

n = int(input())
l = [int(i) for i in input().split()]

print(ppcm(l))
