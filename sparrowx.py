import sys
import math
import copy
import time
import queue
import random
# To debug: print("Debug messages...", file=sys.stderr)
maxCopy=20
maxBareel=100
turnBeforMine=4
turnBeforFire=1
maxStackSize=200

BARREL = 4
mPair=[(1,0),(0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
mImp =[(1,0), (1,-1), (0,-1), (-1,0),  (0,1), (1,1)]
hexAdj=[mPair,mImp]
gameGrid = [[0 for i in range(21)] for j in range(23)]
canons = [[0 for i in range(21)] for j in range(23)]
def rddllt(x,y, radius, filter):
    lower_x = x-radius
    upper_x = x+radius
    li = []
    if (filter):
        for i in range(lower_x, upper_x+1):
            if (validee(i, y)):
                li.append((i, y))
        for i in range(1, radius):
            cur_lower_x = lower_x
            cur_upper_x = upper_x
            cur_y = y-i
            if (cur_y%2==0):
                cur_lower_x += 1
            else:
                cur_upper_x -= 1
            for j in range(cur_lower_x, cur_upper_x+1):
                if (valide(j, cur_y)):
                    li.append((j, cur_y))
                if (valide(j, y+i)):
                    li.append((j, y+i))
    else:
        for i in range(lower_x, upper_x+1):
            li.append((i, y))
        for i in range(1, radius):
            cur_lower_x = lower_x
            cur_upper_x = upper_x
            cur_y = y-i
            if (cur_y%2==0):
                cur_lower_x += 1
            else:
                cur_upper_x -= 1
            for j in range(cur_lower_x, cur_upper_x+1):
                li.append((j, cur_y))
                li.append((j, y+i))
    return li
def findBestMove(ship):
    potentialCells = rddllt(ship.position.x,ship.position.y, 3, True)
    bestScore = -999999999
    bestCell = None
    # Score surrounding cells
    for cell in potentialCells:
        score = 0
        surroundingCells = rddllt(cell[0], cell[1], 5, False)
        for surr_cell in surroundingCells:
            if (not valide(surr_cell[0], surr_cell[1])):
                score -= 1
            else:
                if (gameGrid[surr_cell[0]][surr_cell[1]] != 0):
                    score -= 10
        if (score > bestScore):
            bestScore = score
            bestCell = cell
    if (bestCell is None):
        return (11, 10)
    return bestCell
def valide(x,y):return x>=0 and x<23 and y>=0 and y<21
def bfs(sx, sy):
    q = queue.Queue()
    q.put((sx, sy))
    v = [[False for i in range(21)] for j in range(23)]
    stackConut = 0
    tgt=-100
    best=None
    while(not q.empty()):
        cur = q.get()
        cx = cur[0]
        cy = cur[1]
        if (v[cx][cy]):
            continue
        stackConut += 1
        if (stackConut > maxStackSize):
            break
        if (not valide(cx, cy)):
            continue
        if (gameGrid[cx][cy]> tgt):
            best=cur
            tgt=gameGrid[cx][cy]
        for i in range(6):
            nx = cx
            ny = cy
            nx = cx+hexAdj[cy%2][i][0]
            ny = cy+hexAdj[cy%2][i][1]
            if (not valide(nx, ny)):
                continue
            q.put((nx, ny))
        v[cx][cy] = True
    return best

# OptimizActions
sys.setcheckinterval(1000000)

debug=False
class Case(object):
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.evenDir=[(1,0),(0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
        self.oddDir=[(1,0), (1,-1), (0,-1), (-1,0),  (0,1), (1,1)]
        self.e=None
    def angle(self, targetPosition):
        dy = (targetPosition.y - self.y) * math.sqrt(3) / 2
        dx = targetPosition.x - self.x + ((self.y - targetPosition.y) & 1) * 0.5
        angle = -math.atan2(dy, dx) * 3 / math.pi
        if angle < 0: angle += 6
        elif angle >=6:angle -= 6
        return int(angle)
        
    def toCubeCoordinate(self):
            xp = self.x - (self.y - (self.y & 1)) / 2
            zp = self.y
            yp = -(xp + zp)
            return  Cube(xp, yp, zp)
    def neighbor(self, orientAction):
        if (self.y % 2 == 1):
                newY = self.y + self.oddDir[orientAction][1]
                newX = self.x + self.oddDir[orientAction][0]
        else:
                newY = self.y + self.evenDir[orientAction][1]
                newX = self.x + self.evenDir[orientAction][0]
        return  Case(newX, newY)
    def distanceTo(self,dst): return self.toCubeCoordinate().distanceTo(dst.toCubeCoordinate())
        
    def distance(self,e):return math.sqrt((e.x-self.x)**2+(e.y-self.y)**2)
    def __str__(self):return "{} {}".format(self.x, self.y)
    def valide(self):
        return self.x>=0 and self.x<23 and self.y>=0 and self.y<21
    def equals(self,other):return self.x==other.x and self.y==other.y
class Cube(object):
    def __init__(self,x,y,z):
        self.directions =[(1, -1, 0 ), ( +1, 0, -1 ), ( 0, +1, -1 ), ( -1, +1, 0 ), ( -1, 0, +1 ), ( 0, -1, +1 )]
        self.x,self.y,self.z=x,y,z
    def toOffsetCoordinate(self):
            newX = self.x + (self.z - (self.z & 1)) / 2
            newY = self.z
            return Case(newX, newY)
    def neighbor(self, orientAction):
            nx = self.x + self.directions[orientAction][0]
            ny = self.y + self.directions[orientAction][1]
            nz = self.z + self.directions[orientAction][2]
            return Cube(nx, ny, nz)
    def distanceTo(self,dst):return (abs(self.x - dst.x) + abs(self.y - dst.y) + abs(self.z - dst.z)) // 2
    
class EntityType:
        SHIP, BARREL, MINE, CANNONBALL=0,1,2,3
class Action:
        FASTER, SLOWER, PORT, STARBOARD, FIRE, MINE=0,1,2,3,4,5    
class Entity(object):
    def __init__(self,entityId,x,y):self.entityId,self.position=entityId,Case(x,y)
class Ship(Entity):
    def __init__(self,entityId,arg1,arg2,arg3,arg4,x,y):
        Entity.__init__(self,entityId,x,y)
        self.entityType=EntityType.SHIP
        self.initialHealth=100
        self.orientAction,self.speed,self.health,self.owner=arg1,arg2,arg3,arg4 
        self.mineCooldown=0
        self.cannonCooldown=0
        self.newOrientAction=0
        self.newBowCoordinate=None
        self.newSternCoordinate=None
        self.action=None
        self.target=None
        self.head,self.back=self.computeHeadBack()
    def computeHeadBack(self):
        if self.orientation==0:return Case(x-1,y),Case(x+1,y)
        elif self.orientation==3:return Case(x+1,y),Case(x-1,y)
        elif self.orientation==1:
            if self.position.y%2==0:return Case(x,y-1),Case(x-1,y+1)
            else:return Case(x+1,y-1),Case(x-1,y+1)
        elif self.orientation==4:
            if self.position.y%2==0:return Case(x-1,y+1),Case(x,y-1)
            else:return Case(x-1,y+1),Case(x+1,y-1)
        elif self.orientation==5:
            if self.position.y%2==0:return Case(x,y+1),Case(x-1,y-1)
            else:return Case(x+1,y+1),Case(x,y-1)
        else:
            if self.position.y%2==0:return Case(x,y-1),Case(x-1,y+1)
            else:return Case(x+1,y-1),Case(x-1,y+1)    
    def  moveTo(x,y):
        currentPosition=self.position
        target=Case(x,y)
        if currentPosition.equals(targetPosition):self.action=1;return
        if self.speed==2:self.action=1
        elif self.speed==1:
            #Suppose we've moved first
            currentPosition = currentPosition.neighbor(self.orientAction)
            if (not currentPosition.valide()):self.action =1;return
            #Target reached at next turn
            if (currentPosition.equals(targetPosition)):self.action = None;return
            #For each neighbor cell, find the closest to target
            targetAngle = currentPosition.angle(targetPosition)
            angleStraight = min(abs(self.orientAction - targetAngle), 6 - abs(self.orientAction - targetAngle))
            anglePort = min(abs((self.orientAction + 1) - targetAngle), abs((self.orientAction - 5) - targetAngle))
            angleStarboard = min(abs((self.orientAction + 5) - targetAngle), abs((self.orientAction - 1) - targetAngle))

            centerAngle = currentPosition.angle(Coord(23 // 2, 21 // 2))
            anglePortCenter = min(abs((self.orientAction + 1) - centerAngle), abs((self.orientAction - 5) - centerAngle))
            angleStarboardCenter = min(abs((self.orientAction + 5) - centerAngle), abs((self.orientAction - 1) - centerAngle))
            #Next to target with bad angle, slow down then rotate (avoid to turn around the target!)
            if (currentPosition.distanceTo(targetPosition) == 1 and angleStraight > 1.5):self.action = 1;return

            distanceMin = None
            # Test forward
            nextPosition = currentPosition.neighbor(self.orientAction)
            if (nextPosition.valide()):distanceMin = nextPosition.distanceTo(targetPosition);self.action =None
            #Test port
            nextPosition = currentPosition.neighbor((self.orientAction + 1) % 6)
            if (nextPosition.valide()):
                distance = nextPosition.distanceTo(targetPosition)
                if (distanceMin == None or distance < distanceMin or distance == distanceMin and anglePort < angleStraight - 0.5):
                    distanceMin = distance
                    self.action = 2
                    return
            #Test starboard
            nextPosition = currentPosition.neighbor((self.orientAction + 5) % 6)
            if (nextPosition.valide()):
                distance = nextPosition.distanceTo(targetPosition)
                if (distanceMin == None or distance < distanceMin
                        or (distance == distanceMin and angleStarboard < anglePort - 0.5 and self.action ==2)
                        or (distance == distanceMin and angleStarboard < angleStraight - 0.5 and self.action == None)
                        or (distance == distanceMin and self.action == 2 and angleStarboard == anglePort
                                and angleStarboardCenter < anglePortCenter)
                        or (distance == distanceMin and self.action == 2 and angleStarboard == anglePort
                                and angleStarboardCenter == anglePortCenter and (self.orientAction == 1 or self.orientAction == 4))):
                    distanceMin = distance
                    self.action = 3
                    return
        elif self.speed==1:
            #Rotate ship towards target
            targetAngle = currentPosition.angle(targetPosition)
            angleStraight = min(abs(self.orientAction - targetAngle), 6 - abs(self.orientAction - targetAngle))
            anglePort = min(abs((self.orientAction + 1) - targetAngle), abs((self.orientAction - 5) - targetAngle))
            angleStarboard = min(abs((self.orientAction + 5) - targetAngle), abs((self.orientAction - 1) - targetAngle))

            centerAngle = currentPosition.angle(Coord(23 / 2, 21 / 2))
            anglePortCenter = min(abs((self.orientAction + 1) - centerAngle), abs((self.orientAction - 5) - centerAngle))
            angleStarboardCenter = min(abs((self.orientAction + 5) - centerAngle), abs((self.orientAction - 1) - centerAngle))
            forwardPosition = currentPosition.neighbor(self.orientAction)
            self.action = None

            if (anglePort <= angleStarboard):self.action = 2
          
            if (angleStarboard < anglePort or angleStarboard == anglePort and angleStarboardCenter < anglePortCenter
                    or angleStarboard == anglePort and angleStarboardCenter == anglePortCenter and (self.orientAction == 1 or self.orientAction == 4)):self.action =3
        
            if (forwardPosition.valide() and angleStraight <= anglePort and angleStraight <= angleStarboard):self.action =3

    def faster(self):self.action = 0
    def slower(self) :self.action = 1
    def port(self):self.action =2
    def starboard(self):self.action =3
    def placeMine(self):self.action = 4
    def stern(self) : return self.position.neighbor((self.orientAction + 3) % 6)
    def bow(self):return self.position.neighbor(self.orientAction)
    def newStern(self):self.position.neighbor((self.newOrientAction + 3) % 6)
    def newBow(self):return self.position.neighbor(self.newOrientAction)
    def fire(self,x,y):self.target = Coord(x, y);self.action = 5
    def heal(self, health):
        self.health+=health
        if (self.health > 100):self.health = 100
    def newPositionsIntersect(self, other):
        sternCollision = self.newSternCoordinate != None and (self.newSternCoordinate.equals(other.newBowCoordinate)or self.newSternCoordinate.equals(other.newPosition) or self.newSternCoordinate.equals(other.newSternCoordinate))
        centerCollision =self.newPosition != None and (self.newPosition.equals(other.newBowCoordinate) or newPosition.equals(other.newPosition)or self.newPosition.equals(other.newSternCoordinate))
        return newBowIntersect(other) or sternCollision or centerCollision
    def newPositionsIntersect(self,ships):
        for other in ships:
            if (self != other and self.newPositionsIntersect(other)):return True
        return False
    def damage(self, health):
        self.health -= health
        if (self.health <= 0):self.health= 0

    '''def fire(self,ships):
        global gameGrid
        if self.cannonCooldown!=0:self.updateFire();return None
        for s in ships:
                c=s.position
                d=self.position.distanceTo(c)
                tours=round((d+1)//3)    
                for i in range(tours*s.speed):c=c.neighbor(s.orientAction)
                d=c.distanceTo(self.position)
                if d<=10 and c.valide():self.cannonCooldown=1;gameGrid[c.x][c.y]=50;return Fire(c.x,c.y)
        return None'''

class Damage(object):
    def __init__(self,position,health,hit):self.position,self.health,self.hit=position,health,hit

class Barrel(Entity):
    def __init__(self,entityId,arg1,x,y):
        self.entityType=EntityType.BARREL
        Entity.__init__(self,entityId,x,y)
        self.health=arg1

class Mine(Entity):
    def __init__(self,entityId,x,y):
        Entity.__init__(self,entityId,x,y)
        self.entityType=EntityType.MINE
    def explode(self,ships, force):
        damage = []
        victim = None

        for ship in ships:
            if position.equals(ship.bow()) or position.equals(ship.stern()) or position.equals(ship.position):
	            damage +=[Damage(self.position, 25, True)]
	            ship.damage(25)
	            victim = ship

        if (force or victim != None):
            if (victim == None):damage +=[Damage(self.position, 25, True)]
            for ship in ships:
                if (ship != victim) :
                    impactPosition = None
                    if (ship.stern().distanceTo(position) <= 1):impactPosition = ship.stern()
                    if (ship.bow().distanceTo(position) <= 1):impactPosition = ship.bow();
                    if (ship.position.distanceTo(position) <= 1):impactPosition = ship.position
                    if (impactPosition != null):
                        ship.damage(10)
                        damage +=[Damage(impactPositionn, 10, True)]

        return damage
class Cannoball(Entity):
    def __init__(self,x,y,ownerEntityId,srcX,srcY,remainingTurns):
            Entity.__init__(self,x,y)
            self.entityType=EntityType.CANNONBALL
            self.srcX,self.srcY=srcX,srcY
            self.ownerEntityId,self.remainingTurns,self.initialRemainingTurns=ownerEntityId,remainingTurns,remainingTurns
class Action(object):
    def __init__(self,x,y):self.x,self.y=x,y
class Move(Action):
     def __init__(self,x,y):Action.__init__(self,x,y)
     def __str__(self):return "MOVE {} {}".format(self.x, self.y)
     def utility(self,player):return maxBareel-payer.ships[-1].health+1
     
class Fire(Action):
     def __init__(self,x,y):Action.__init__(self,x,y)
     def __str__(self):return "FIRE {} {}".format(self.x, self.y)
     def utility(self):return 1
class Port(Action):
    def __init__(self,x,y):Action.__init__(self,x,y)
    def __str__(self):return "PORT"
    
class Starboard(Action):
    def __init__(self,x,y):Action.__init__(self,x,y)
    def __str__(self):return "Starboard"
    
class Faster(Action):
    def __init__(self,x,y):Action.__init__(self,x,y)
    def __str__(self):return "Faster"

class Slower(Action):
    def __init__(self,x,y):Action.__init__(self,x,y)
    def __str__(self):return "Slower"
    
class Wait(Action):
    def __init__(self,x,y):Action.__init__(self,x,y)
    def __str__(self):return "Wait"
class Fire(Wait):
    def __init__(self,x,y):Wait.__init__(self,x,y)
    def __str__(self):return "MINE"
        
class Player(object):
    
    def __init__(self,player,ships):self.player,self.ships=player,ships
    def play(self,game):
        actions=[]
        global gameGrid
        for s in self.ships:
             tmp=-50
             mm=Move(11,10)
             #for a in actions:
             #   if a and gameGrid[a.x][a.y]>tmp:mm=a;tmp=gameGrid[a.x][a.y]
             print(mm)
             
class Game(object):
    def __init__(self):
        self.players,self.mines,self.barrels,self.cannonballs=[Player(0,[]),Player(1,[])],[],[],[]
        self.cannonBallExplosions=[]
        self.damage=[]
        self.turn=0
    def updateInput(self):
        global gameGrid
        gameGrid=[[0 for i in range(21)] for j in range(23)]
        self.mines,self.barrels=[],[]
        my_ship_count = int(input())  # the number of remaining ships
        entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
        if self.turn==0:
            for i in range(entity_count):
                entity_id, entityType, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
                entity_id = int(entity_id)
                x = int(x)
                y = int(y)
                arg_1 = int(arg_1)
                arg_2 = int(arg_2)
                arg_3 = int(arg_3)
                arg_4 = int(arg_4)
                if entityType =='SHIP':self.players[arg_4].ships+=[Ship(entity_id,arg_1, arg_2, arg_3, arg_4,x,y)]
                elif entityType =='BARREL':self.barrels+=[Barrel(entity_id,arg_1,x,y)]
                elif entityType =='MINE':self.mines+=[Mine(entity_id,x,y)]
        else:
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
                    ship=filter(lambda x: x.entityId == entity_id, self.players[arg_4].ships)
                    if ship:=ship.orientation,ship.speed,ship.health,ship.position= arg_1, arg_2, arg_3,Case(x,y)
                elif entityType =='BARREL':self.barrels+=[Barrel(entity_id,arg_1,x,y)]
                elif entityType =='CANNONBALL':
                    ball=filter(lambda x: x.entityId == entity_id, self.cannonballs)
                    if ball:ball.remainingTurns=arg2
                    else:
                        ship=filter(lambda x: x.entityId == arg1, self.players[0].ships+self.players[1].ships)
                        head=ship.computeHeadBack()[0]
                        source=head.position
                        self.cannonballs+=[Cannoball(entity_id,x,y,arg_1,source.x,source.y,arg_2)]
                elif entityType =='MINE':self.mines+=[Mine(entity_id,x,y)]
            
        self.turn+=1
    def decrementRum(self):
        ships=self.players[0].ships+self.players[1].ships
        for ship in self.ships:ship.damage(1)
    def updateInitialRum(self):
        ships=self.players[0].ships+self.players[1].ships
        for ship in ships:
            ship.initialHealth = ship.health
    def moveCannonballs(self):
        for ball in self.cannonballs:
            if (ball.remainingTurns == 0):del canon;continue
            elif ball.remainingTurns > 0 :ball.remainingTurns-=1
            if (ball.remainingTurns == 0):self.cannonBallExplosions+=[ball.position]
    def checkBarrelCollisions(self, ship):
        bow = ship.bow()
        stern = ship.stern()
        center = ship.position
        for barrel in self.barrels:
            if (barrel.position.equals(bow) or barrel.position.equals(stern) or barrel.position.equals(center)):ship.heal(barrel.health);del barrel
    def checkMineCollisions(self):
        ships=self.players[0].ships+self.players[1].ships
        for min in self.mines:
            mineDamage = mine.explode(ships, False)
            if len(mineDamage)>0:damage+=mineDamage
    def checkCollisions(self):
        ships=self.players[0].ships+self.players[1].ships
        # Check collisions with Barrels
        for ship in ships:checkBarrelCollisions(ship)
        # Check collisions with Mines
        checkMineCollisions()

    def moveShips(self):
        ships=self.players[0].ships+self.players[1].ships
        for  i in range(1,3):
            for ship in ships:
                ship.newPosition = ship.position
                ship.newBowCoordinate = ship.bow()
                ship.newSternCoordinate = ship.stern()
                if (i > ship.speed):continue
                newCoordinate = ship.position.neighbor(ship.orientAction)
                if (newCoordinate.valide()):
                    # Set new coordinate.
                    ship.newPosition = newCoordinate
                    ship.newBowCoordinate = newCoordinate.neighbor(ship.orientAction)
                    ship.newSternCoordinate = newCoordinate.neighbor((ship.orientAction + 3) % 6)
                else:
                    #Stop ship!
                    ship.speed = 0

            #Check ship and obstacles collisions
            collisions = []
            collisionDetected = True
            while (collisionDetected):
                collisionDetected = False
                for ship in ships:
                    if (ship.newBowIntersect(ships)):collisions.add(ship)

                for ship in collisions:
                    # Revert last move
                    ship.newPosition = ship.position
                    ship.newBowCoordinate = ship.bow()
                    ship.newSternCoordinate = ship.stern()
                    ship.speed = 0
                    collisionDetected = True
                
                collisions=[]
                #Move ships to their new locAction
                for ship in ships : ship.position = ship.newPosition
            self.checkCollisions()
    def rotateShips(self):
        ships=self.players[0].ships+self.players[1].ships
        #Rotate
        for  ship in ships:
            ship.newPosition = ship.position
            ship.newBowCoordinate = ship.newBow()
            ship.newSternCoordinate = ship.newStern()
        #Check collisions
        collisionDetected = True
        collisions =[]
        while (collisionDetected):
            collisionDetected = False
            for ship in ships:
                if (ship.newPositionsIntersect(ships)):collisions+=[ship]
            for ship in collisions:
	            ship.newOrientAction = ship.orientAction
	            ship.newBowCoordinate = ship.newBow()
	            ship.newSternCoordinate = ship.newStern()
	            ship.speed = 0
	            collisionDetected = True
            collisions=[]
        #Apply rotAction
        for ship in ships:ship.orientAction = ship.newOrientAction
        self.checkCollisions()

    def gameIsOver(self):
        for player in self.players: 
            if len(self.player.ships)==0:return True
        return len(self.barrels) == 0 and self.turn==200

    def explodeShips(self):
        ships=self.players[0].ships+self.players[1].ships
        for position in self.cannonBallExplosions:
            for ship in ships:
                if (position.equals(ship.bow()) or position.equals(ship.stern())):
                    self.damage+=[Damage(position, 25, True)]
                    ship.damage(25)
                    del position
                    break
                elif (position.equals(ship.position)):
                    self.damage+=[Damage(position, 25, True)]
                    ship.damage(50)
                    del position
                    break
    def explodeMines(self):
        ships=self.players[0].ships+self.players[1].ships
        for ball in self.cannonBallExplosions:
            for mine in self.mines:
                if (mine.position.equals(ball)):
                    self.damage+=mine.explode(ships, True)
                    del mine
                    del ball
                    break
    def explodeBarrels(self):
        for ball in self.cannonBallExplosions:
            for Barrel in self.barrels:
                if (barrel.position.equals(position)):
                    self.damage+=[Damage(position, 0, True)]
                    del ball
                    del bareel
                    break
    def updateGame(self):
        self.moveCannonballs()
        self.decrementRum()
        self.updateInitialRum()

        self.applyActions()
        self.moveShips()
        self.rotateShips()

        self.explodeShips()
        self.explodeMines()
        self.explodeBarrels()

        #For each sunk ship, create a new rum barrel with the amount of rum the ship had at the begin of the turn (up to 30).
        for ship in ships:
            if (ship.health <= 0):
                reward = min(30, ship.initialHealth)
                if (reward > 0):self.barrels+=[Barrel(ship.position.x, ship.position.y, reward)];del ship
       
        for position in cannonBallExplosions:damage+=[Damage(position, 0, True)]
           

    
    def applyActions(self):
        ships=self.players[0].ships+self.players[1].ships
        for ship in ships:
            if ship.mineCooldown>0:ship.mineCooldown-=1
            if ship.cannonCooldown>0:ship.cannonCooldown-=1
            ship.newOrientAction = ship.orientAction
            if (ship.action != None):
                if ship.action==0:
                    if (ship.speed < 2):ship.speed+=1
                elif ship.action==1:
                    if (ship.speed >0):ship.speed-=1
                elif ship.action==2:ship.newOrientAction = (ship.orientAction + 1) % 6
                elif ship.action==3:ship.newOrientAction = (ship.orientAction + 3) % 6
            elif ship.action==4:
                 if (ship.mineCooldown == 0):
                    target = ship.stern().neighbor((ship.orientAction + 3) % 6)
                    if (target.valide()):
                        cellIsFreeOfBarrels=None
                        cellIsFreeOfMines=None
                        cellIsFreeOfShips=None
                        for barrel in self.barrels:cellIsFreeOfBarrels=not barrel.position.equals(target)
                        for mine in self.mines:cellIsFreeOfMines = not mine.position.equals(target)
                        for oShip in ships:cellIsFreeOfShips = (oShip!=ship and not oShip.position.equals(target))
                        if (cellIsFreeOfBarrels and  cellIsFreeOfShips and cellIsFreeOfMines):
                            ship.mineCooldown = 5
                            self.mines+=[Mine(target.x, target.y)]
            elif ship.action==5:
                distance = ship.bow().distanceTo(ship.target)
                if (ship.target.valide() and distance <= 10 and ship.cannonCooldown == 0):
                    travelTime = (int) (1 + round(ship.bow().distanceTo(ship.target) / 3.0))
                    cannonballs+=[Cannonball(ship.target.x, ship.target.y, ship.id, ship.bow().x, ship.bow().y, travelTime)]
                    ship.cannonCooldown=2
    def clone(self): 
        g=Game()
        g.players=copy.copy(self.players)    
        g.turn=copy.copy(self.turn)
        g.barrels=copy.copy(self.barrels)
        g.cannonBallExplosions=copy.copy(self.cannonBallExplosions)
        g.mines=copy.copy(self.mines) 
        g.damage=copy.copy(self.damage)          
  
g=Game()
# game loop
while True:
    time_t = time.time()
    g.updateInput()
    g.players[-1].play(g)
    time_t = time.time()-time_t
    print("Debug messages...",time_t, file=sys.stderr)