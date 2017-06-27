import sys
import math
from itertools import count

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())

ref = set(str(n))
for i in count(n+1):
    if ref.isdisjoint(set(str(i))):
        print(i)
        break
