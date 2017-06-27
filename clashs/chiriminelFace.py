import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

hair, cheek, eye, nose, mouth, chin = raw_input().split()

# Write an action using print
# To debug: print >> sys.stderr, "Debug messages..."

print hair*5
print cheek+eye+" "+eye+cheek
print cheek+" "+nose+" "+cheek
print cheek+" "+mouth+" "+cheek
if len(chin)==1:print "  "+chin+""
elif len(chin)>=2 and len(chin)<5:print " "+chin+""
else:print chin