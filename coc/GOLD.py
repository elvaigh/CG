import sys
import math
import copy
import time
import queue
import random
# Optimizations
sys.setcheckinterval(1000000)
debug=False

# To debug: print("Debug messages...", file=sys.stderr)



############################################################################
######################### GENETIQUE ########################################
############################################################################
tailleP=7
generationsMax=10
pnull=0.6
pbon=0.4
NBbons=int(pbon*tailleP)
milieu=1
actions_autorises = [0,1,2,3,4,5,6,7]

def chance_mutation(x): return 0.3/x
def choix(x):x[random.randint(0,len(x))]
def obtenir_caractere_alea(): return random.randint(0,23)
def obtenir_individu_alea(ship): 
    individu=[obtenir_caractere_alea()%7,obtenir_caractere_alea(),obtenir_caractere_alea()%21]
    return [individu,obtenir_score(individu,ship)]
def obtenir_population_alea(ship): return [obtenir_individu_alea(ship) for _ in range(nb_population)]
def obtenir_score(individu,ship):
    # tmp=copy.copy(gameGrid)
    # simulate(tmp,individu,ship)
    # for ship in ships:score+=ship[0]*ship[1]
    return sum(individu)#score


 #----Fonction qui classe les individus en fonction de leur score
def classement_population(population,ship): 
    for individu in population: #Pour chaque individu dans la population
        individu[1]=obtenir_score(individu[0],ship) #on ajoute à la fin de cette liste le tuple (individu, score)
    return sorted(population, key=lambda x: x[1], reverse=True) #On trie la liste des individus selon la case "score" (donc 1 du tuple) et on l'inverse pour avoir un ordre décroissant et non pas croissant.


#----Fonction primordiale qui fait évoluer, muter, etc la population
def evolution_population(population,ship): 
    
    population_classee = classement_population(population,ship)
    # Filtrage des meilleurs candidats
    parents = population_classee[:NBbons] #Les parents (= ceux qui pourront se "reproduire") sont les meilleurs individus

    # Sauvetage de chanceux
    for individu in population_classee[NBbons:]: #Pour chaque individu parmi les non-meilleurs
        if random.random() < pbon: #On jette un dé pour savoir s'il est sauvé
            parents.append(individu) #Si oui on l'ajoute à la liste des parents
    # Mutations
    for individu in parents: #Pour chaque individu parmi les parents
        if  individu[1]<= 0:
            mutation = 1
        else:
            mutation = chance_mutation(1/max(1,individu[1]))
        if random.random() < mutation: #On jette un dé pour savoir s'il subit une mutation
            caractere_a_modifier = int(random.random() * 3) #Si oui, on tire au pif le caractère à muter
            crt=obtenir_caractere_alea() 
            if caractere_a_modifier==0:crt=crt%8
            elif caractere_a_modifier==2:crt=crt%21
            print("individu muté",individu, file=sys.stderr)
            individu[0][caractere_a_modifier]= crt#et on le remplace par un autre au hasard
    
    # Reproduction
    nb_parents = len(parents)                   #On enregistre le nombre de parents
    nb_enfants = nb_population - nb_parents     #Le nombre de nouveaux individus est égal au nombre d'individus maximum dans la population moins le nombre de parents, qui font partie de cette nouvelle population
    enfants = []
    i=0
    while i < nb_enfants:            #Tant que le nombre d'enfants est inférieur au nombre d'enfants attendus
        papa = choix(parents)                  #On choisit un papa
        maman = choix(parents)               #et une maman
        print("parents",papa,maman, file=sys.stderr)
        if papa != maman:                       #On vérifie qu'on a bien 2 individus différents, sinon on obtient un nouvel individu identique
            enfant = papa[0][:milieu] + maman[0][milieu:] #Un enfant est composé de la première moitié du père et de la seconde moitié de la mère
            enfants.append([enfant,(papa[1]+maman[1])//2])              #On ajoute le nouvel individu à la liste des enfants
            i+=1
    population = parents
    
    population.extend(enfants)        #La nouvelle population est constituée des parents ainsi que des enfants        
    return population

def algo_gen(ship):
    i=0
    population = obtenir_population_alea(ship)
   
    print("population initiale",population,file=sys.stderr)
    # time_t = time.time()
    while i < generationsMax:
        #print("Debug messages...",population," No",i, file=sys.stderr)
        population = evolution_population(population,ship)
        i+=1
    #     # time_t = time.time()-time_t
    p=tmp[0]
    return p[0][0],p[0][1],p[0][2]
##########################################################################
#########################  HELPER ########################################
##########################################################################
maxCopy=20
maxBareel=100
turnBeforMine=5
turnBeforFire=2
maxStackSize=500
mPair=[(1,0),(0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
mImp =[(1,0), (1,-1), (0,-1), (-1,0),  (0,1), (1,1)]
hexAdj=[mPair,mImp]
SHIP=100
ACTIONS=['WAIT','FASTER', 'SLOWER', 'PORT', 'STARBOARD', 'MINE','FIRE','MOVE']
turn=0
cannonGrid=[[0 for i in range(21)] for j in range(23)]
gameGrid = [[0 for i in range(21)] for j in range(23)]
ships=[]
myships=[]
BARREL=5
MYSHIP=200
my_ship_count=0
def valide(x,y):return x>=0 and x<23 and y>=0 and y<21
def bfs(sx, sy,target):
    curScore=-9999
    q = queue.Queue()
    q.put((sx, sy))
    v = [[False for i in range(21)] for j in range(23)]
    stackConut = 0
    while(not q.empty()):
        cur = q.get()
        cx = cur[0]
        cy = cur[1]
        if (v[cx][cy]):continue
        stackConut += 1
        if (stackConut > maxStackSize):break
        if (valide(cx, cy)):
            if ( target==gameGrid[cx][cy]):return cur
            for i in range(6):
                nx = cx+hexAdj[cy%2][i][0]
                ny = cy+hexAdj[cy%2][i][1]
                if valide(nx, ny):q.put((nx, ny))
            v[cx][cy] = True
        #print("Debug messages...",curScore,stackConut,cur,target, file=sys.stderr)
    return None

def distTo(x1, y1, x2, y2):
    xp1 = x1 - (y1 - (y1 & 1)) / 2
    zp1 = y1
    yp1 = -(xp1 + zp1)
    xp2 = x2 - (y2 - (y2 & 1)) / 2
    zp2 = y2
    yp2 = -(xp2 + zp2)
    return (abs(xp1 - xp2) + abs(yp1 - yp2) + abs(zp1 - zp2)) / 2
def simulate(gride,individu,ship):
    action=individu[0]
    if action==0:
       if valide(ship[2]+1,ship[3]): gride[(ship[2]+1,ship[3])]=MYSHIP;gride[(ship[2],ship[3])]=0
    elif action==1:
       if valide(ship[2]-1,ship[3]):gride[(ship[2]-1,ship[3])]=MYSHIP;gride[(ship[2],ship[3])]=0
    elif action==2:
        if valide(ship[2],ship[3]-1):gride[(ship[2],ship[3])-1]=MYSHIP;gride[(ship[2],ship[3])]=0
    elif action==3:
        if valide(ship[2],ship[3]+1):gride[(ship[2],ship[3])+1]=MYSHIP;gride[(ship[2],ship[3])]=0
    elif action==4:
        gride[back(x,y,ship[4])]=-50
    elif action==5:
        d=distTo(individu[1],individu[1], ship[2],ship[3])
        ttt=1+d//3
        if ttt<10:ship[1]=min(ship[1]+25,100)
    elif action==6:
        t=bfs(individu[1],individu[1],BARREL)
        if t:gride[(individu[1],individu[1])]=0;ship[1]=min(ship[1]+t,100)

def back(x,y,orientAction):
    if orientAction==0:(x+1,y)
    elif orientAction==3:return (x-1,y)
    elif orientAction==1:
        if y%2==0:return (x-1,y+1)
        else:return (x-1,y+1)
    elif orientAction==4:
        if y%2==0:return (x,y-1)
        else:return (x+1,y-1)
    elif orientAction==5:
        if y%2==0:return (x-1,y-1)
        else:return (x,y-1)
    else:
        if y%2==0:return (x-1,y+1)
        else:return (x-1,y+1)    

##########################################################################
#########################  O/I ########################################
##########################################################################

def updateGrid():
    ships=[]
    myships=[]
    gameGrid = [[0 for i in range(21)] for j in range(23)]
    my_ship_count = int(input())  # the number of remaining ships
    entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
    for i in range(entity_count):
        entity_id, entityType, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        if entityType =='SHIP':
            gameGrid[x][y]=(1+arg_4)*SHIP
            if arg_4==0:arg_4=-1
            ships+=[[arg_4,arg_3,x,y,arg_1]]
        elif entityType =='BARREL':gameGrid[x][y]=BARREL
        elif entityType =='MINE' :gameGrid[x][y]=-50
        elif entityType =='CANNONBALL' and arg_2==2:gameGrid[x][y]=-50
def output_gen(genome):
    if genome[0]==5 or genome[0]==6:print(ACTIONS[genome[0]],genome[1],genome[2])
    else:print(ACTIONS[genome[0]])
def output():
    for i in range(my_ship_count):output_gen(algo_gen(myships[i]))
    
# game loop
while True:
    turn+=1
    time_t = time.time()
    updateGrid()
    output()
    time_t = time.time()-time_t
    print("Debug messages...",time_t, file=sys.stderr)