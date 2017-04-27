import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# nb_floors: number of floors
# width: width of the area
# nb_rounds: maximum number of rounds
# exit_floor: floor on which the exit is found
# exit_pos: position of the exit on its floor
# nb_total_clones: number of generated clones
# nb_additional_elevators: ignore (always zero)
# nb_elevators: number of elevators
nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in raw_input().split()]
x=[]
l={}
for i in xrange(nb_elevators):
    # elevator_floor: floor on which this elevator is found
    # elevator_pos: position of the elevator on its floor
    x=([int(j) for j in raw_input().split()])
    l[x[0]]=x[1]
i=0
j=0
k=0
# game loop
while True:
    # clone_floor: floor of the leading clone
    # clone_pos: position of the leading clone on its floor
    # direction: direction of the leading clone: LEFT or RIGHT
    clone_floor, clone_pos, direction = raw_input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)
    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."
    #print >> sys.stderr, "Debug messages...",direction,clone_pos,clone_floor,l[clone_floor],clone_pos
    if  clone_floor!=exit_floor and clone_floor>=j and ( (l[clone_floor]<clone_pos and direction=="RIGHT") or (l[clone_floor]>clone_pos and direction=="LEFT")):
        print "BLOCK"
        k=0
        j+=1
    elif clone_floor==exit_floor and ((exit_pos>clone_pos  and direction=="LEFT") or (exit_pos<clone_pos  and direction=="RIGHT")) :
     print "BLOCK"
    else:
     print "WAIT"
     
        
        
    
    # action: WAIT or BLOCK
    
