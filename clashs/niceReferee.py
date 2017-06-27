import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

l, r, h = [int(i) for i in raw_input().split()]
print >> sys.stderr,l,r,h
# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print max(int(math.sqrt((r)**2+h**2)),int(math.sqrt((l-r)**2+h**2)))
