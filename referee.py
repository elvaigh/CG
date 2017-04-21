import re

class Coord(object):
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
            return  CubeCoordinate(xp, yp, zp)
    def neighbor(self, orientAction):
        if (self.y % 2 == 1):
                newY = self.y + self.oddDir[orientAction][1]
                newX = self.x + self.oddDir[orientAction][0]
        else:
                newY = self.y + self.evenDir[orientAction][1]
                newX = self.x + self.evenDir[orientAction][0]
        return  Coord(newX, newY)
    def distanceTo(self,dst): return self.toCubeCoordinate().distanceTo(dst.toCubeCoordinate())
        
    def distance(self,e):return math.sqrt((e.x-self.x)**2+(e.y-self.y)**2)
    def __str__(self):return "{} {}".format(self.x, self.y)
    def valide(self):
        return self.x>=0 and self.x<23 and self.y>=0 and self.y<21
    def equals(self,other):return self.x==other.x and self.y==other.y
class CubeCoordinate(object):
    def __init__(self,x,y,z):
        self.directions =[(1, -1, 0 ), ( +1, 0, -1 ), ( 0, +1, -1 ), ( -1, +1, 0 ), ( -1, 0, +1 ), ( 0, -1, +1 )]
        self.x,self.y,self.z=x,y,z
    def toOffsetCoordinate(self):
            newX = self.x + (self.z - (self.z & 1)) / 2
            newY = self.z
            return Coord(newX, newY)
    def neighbor(self, orientAction):
            nx = self.x + self.directions[orientAction][0]
            ny = self.y + self.directions[orientAction][1]
            nz = self.z + self.directions[orientAction][2]
            return CubeCoordinate(nx, ny, nz)
    def distanceTo(self,dst):return (abs(self.x - dst.x) + abs(self.y - dst.y) + abs(self.z - dst.z)) // 2

class EntityType:
        SHIP, BARREL, MINE, CANNONBALL=0,1,2,3
class Action:
        FASTER, SLOWER, PORT, STARBOARD, FIRE, MINE=0,1,2,3,4,5

class Entity(object):
    UNIQUE_ENTITY_ID = 0
    def __init__(self,Type,x,y):
        UNIQUE_ENTITY_ID+=1
        self.entityId,self.Type,self.position=UNIQUE_ENTITY_IDyId,Type,Case(x,y)
class Mine(Entity):
    def __init__(self,x,y):Entity.__init__(self,EntityType.MINE,x,y)
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
        Entity.__init__(self,EntityType.CANNONBALL,x,y)
        self.srcX,self.srcY=srcX,srcY
        self.ownerEntityId,self.remainingTurns,self.initialRemainingTurns=ownerEntityId,remainingTurns,remainingTurns
class RumBarrel(Entity):
    def __init__(self,entityId,health,x,y):
        Entity.__init__(self,EntityType.BARREL,x,y)
        self.health=health
class Damage(object):
    def __init__(self,position,health,hit):self.position,self.health,self.hit=position,health,hit
class Ship(Entity):
    def __init__(self,entityId,arg1,arg2,arg3,arg4,x,y):
        Entity.__init__(self,entityId,x,y)
        self.initialHealth=100
        self.orientAction,self.speed,self.health,self.owner=arg1,arg2,arg3,arg4 
        self.mineCooldown=0
        self.cannonCooldown=0
        self.newOrientAction=0
        self.newBowCoordinate=None
        self.newSternCoordinate=None
        self.action=None
        self.target=None
        
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
class Player(object):
    def __init__(self,id):self.id,self.ships,self.shipsAlive=id,[],[]

    def setDead(self):
        for ship in self.ships:ship.health = 0
    def getScore(self):
        score=0
        for ship in self.ships score += ship.health
       return score

class Referee(object):
    
    def __init__(self):
        self.seed=123456789
        self.MAP_WIDTH=23
        self.MAP_HEIGHT=21
        self.COOLDOWN_CANNON = 2
        self.COOLDOWN_MINE = 5
        self.INITIAL_SHIP_HEALTH = 100
        self.MAX_SHIP_HEALTH = 100
        self.MAX_SHIP_SPEED=2
        self.MIN_SHIPS = 1
        self.MAX_SHIPS=3
        self.MIN_MINES=5
        self.MAX_MINES=10
        self.MIN_RUM_BARRELS = 10
        self.MAX_RUM_BARRELS = 26
        self.MIN_RUM_BARREL_VALUE = 10
        self.MAX_RUM_BARREL_VALUE = 20
        self.REWARD_RUM_BARREL_VALUE = 30
        self.MINE_VISIBILITY_RANGE = 5
        self.FIRE_DISTANCE_MAX = 10
        self.LOW_DAMAGE = 25
        self.HIGH_DAMAGE = 50
        self.MINE_DAMAGE = 25
        self.NEAR_MINE_DAMAGE = 10
        self.CANNONS_ENABLED=True
        self.MINES_ENABLED=True
        self.random=0
        self.mineCount=0

        self.PLAYER_INPUT_MOVE_PATTERN = re.compile("MOVE (?<x>-?[0-9]{1,8})\\s+(?<y>-?[0-9]{1,8})(?:\\s+(?<message>.+))?",flags=re.IGNORECASE)
        self.PLAYER_INPUT_SLOWER_PATTERN = Pattern.compile("SLOWER(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)
        self.PLAYER_INPUT_FASTER_PATTERN = Pattern.compile("FASTER(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)
        self.PLAYER_INPUT_WAIT_PATTERN = Pattern.compile("WAIT(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)
        self.PLAYER_INPUT_PORT_PATTERN = Pattern.compile("PORT(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)
        self.PLAYER_INPUT_STARBOARD_PATTERN = Pattern.compile("STARBOARD(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)
        self.PLAYER_INPUT_FIRE_PATTERN = Pattern.compile("FIRE (?<x>-?[0-9]{1,8})\\s+(?<y>-?[0-9]{1,8})(?:\\s+(?<message>.+))?",flags=re.IGNORECASE)
        self.PLAYER_INPUT_MINE_PATTERN = Pattern.compile("MINE(?:\\s+(?<message>.+))?", flags=re.IGNORECASE)

        self.players,self.mines,self.barrels,self.cannonballs,self.cannonBallExplosions,self.damage,self.turn=[],[],[],[],[],[],0
    def initReferee(playerCount, prop) :
        self.seed = self.parseProperty(prop, "seed", random.seed(datetime.now()))
        self.random = random.seed(self.seed)
        shipsPerPlayer = self.clamp(int(self.parseProperty(prop, "shipsPerPlayer", random.randInt(1 + self.MAX_SHIPS - self.MIN_SHIPS) + self.MIN_SHIPS)), self.MIN_SHIPS,self.MAX_SHIPS)

        if (self.MAX_MINES > self.MIN_MINES):
            self.mineCount = self.clamp(int(self.parseProperty(prop, "mineCount", random.nextInt(MAX_MINES - MIN_MINES) + MIN_MINES)), MIN_MINES, MAX_MINES)
        else:mineCount = self.MIN_MINES
        self.self.barrelCount = self.clamp(int(self.parseProperty(prop, "barrelCount", random.randInt(self.MAX_RUM_BARRELS - self.MIN_RUM_BARRELS) + self.MIN_RUM_BARRELS)),self.MIN_RUM_BARRELS, self.MAX_RUM_BARRELS)
        
        cannonballs = []
        cannonBallExplosions = []
        damage =[]

        # Generate Players
        self.players = []
        for i in range(self.playerCount):self.players+=[Player(i)]
        
        #Generate Ships
        for j in range(self.shipsPerPlayer):
            xMin = 1 + j * self.MAP_WIDTH // self.shipsPerPlayer;
            xMax = (j + 1) * self.MAP_WIDTH // self.shipsPerPlayer - 2

            y = 1 + random.nextInt(MAP_HEIGHT // 2 - 2)
            x = xMin + random.nextInt(1 + xMax - xMin)
            orientation = random.randInt(0,6)

            ship0 = Ship(x, y, orientation, 0)
            ship1 = Ship(x, self.MAP_HEIGHT - 1 - y, (6 - orientation) % 6, 1)

            self.players[0].ships+=[ship0]
            self.players[1].ships+=[ship1]
            self.players[0].shipsAlive+=[ship0]
            self.players[0].shipsAlive+=[ship1]

        self.ships = self.players[0]+self.players[1]

        #Generate mines
        self.mines = []
        while len(self.mines)< self.mineCount:
            x = 1 + random.randInt(0,self.MAP_WIDTH - 2)
            y = 1 + random.randInt(0,self.MAP_HEIGHT // 2)

            m = Mine(x, y)

            cellIsFreeOfMines = mines.stream().noneMatch(mine -> mine.position.equals(m.position));
            cellIsFreeOfShips = ships.stream().noneMatch(ship -> ship.at(m.position));

            if (cellIsFreeOfShips && cellIsFreeOfMines) {
                if (y != self.MAP_HEIGHT - 1 - y):self.mines+=[Mine(x, self.MAP_HEIGHT - 1 - y)]
                self.mines+=[m]
        self.mineCount =len(self.mines)

        #Generate supplies
        barrels = []
        while (len(barrels)< self.barrelCount) :
            x = 1 + random.randInt(MAP_WIDTH - 2)
            y = 1 + random.randInt(MAP_HEIGHT // 2)
            h = self.MIN_RUM_BARREL_VALUE + random.randInt(0,1 + self.MAX_RUM_BARREL_VALUE - self.MIN_RUM_BARREL_VALUE)
            m = RumBarrel(x, y, h);
            cellIsFreeOfBarrels = barrels.stream().noneMatch(barrel -> barrel.position.equals(m.position));
            cellIsFreeOfMines = mines.stream().noneMatch(mine -> mine.position.equals(m.position));
            cellIsFreeOfShips = ships.stream().noneMatch(ship -> ship.at(m.position));
            if (cellIsFreeOfShips && cellIsFreeOfMines && cellIsFreeOfBarrels) {
                if (y != self.MAP_HEIGHT - 1 - y): barrels+=[RumBarrel(x, self.MAP_HEIGHT - 1 - y, h)]
                barrels+=[m]
        barrelCount = barrels.size()

    def clamp(int val, int min, int max):
        return max(min, min(max, val))

    def parseProperty(prop, key, defaultValue):
        try:return Long.valueOf(prop.getProperty(key));
        except NumberFormatException e:#Ignore invalid data
        return defaultValue
    def getConfiguration():
        prop = Properties()
        prop.setProperty("seed", int(self.seed))
        prop.setProperty("shipsPerPlayer", int(self.shipsPerPlayer))
        prop.setProperty("barrelCount", int(self.barrelCount))
        prop.setProperty("mineCount", int(self.mineCount))
        return prop
    def prepare(self, round):
        for player in self.players:
            for ship in player.ship:ship.action=None
        self.cannonBallExplosions=[]
        self.damage=[]
    def getExpectedOutputLineCountForPlayer(self,playerIdx):return len(self.players[playerIdx].shipsAlive)
    def handlePlayerOutput(self,frame, round, playerIdx, outputs):
        player = self.players[playerIdx]
        try :
            i=0
            for line in outputs:
                matchWait = self.PLAYER_INPUT_WAIT_PATTERN.matcher(line)
                matchMove = self.PLAYER_INPUT_MOVE_PATTERN.matcher(line)
                matchFaster = self.PLAYER_INPUT_FASTER_PATTERN.matcher(line)
                matchSlower = self.PLAYER_INPUT_SLOWER_PATTERN.matcher(line)
                matchPort =self.PLAYER_INPUT_PORT_PATTERN.matcher(line)
                matchStarboard = self.PLAYER_INPUT_STARBOARD_PATTERN.matcher(line)
                matchFire = self.PLAYER_INPUT_FIRE_PATTERN.matcher(line)
                matchMine = self.PLAYER_INPUT_MINE_PATTERN.matcher(line)
                ship = player.shipsAlive[i];i+=1
                if (matchMove.matches()):
                    x=int(matchMove.group("x"))
                    y=int(matchMove.group("y"))
                    ship.moveTo(x, y)
                elif(matchFaster.matches()):
                    #ship.setMessage(matchFaster.group("message"));
                    ship.faster()
                elif(matchSlower.matches()):
                    #ship.setMessage(matchSlower.group("message"));
                    ship.slower()
                elif(matchPort.matches()):
                    #ship.setMessage(matchPort.group("message"));
                    ship.port()
                elif(matchStarboard.matches()):
                    #ship.setMessage(matchStarboard.group("message"));
                    ship.starboard()
                elif(matchWait.matches()):
                    #ship.setMessage(matchWait.group("message"));
                elif(matchMine.matches()):
                    #ship.setMessage(matchMine.group("message"));
                    ship.placeMine()
                elif(matchFire.matches()):
                    x=int(matchFire.group("x"))
                    y=int(matchFire.group("y"))
                    #ship.setMessage(matchFire.group("message"));
                    ship.fire(x, y)
                else:print(InvalidInputException("A valid action", line))
        except InvalidInputException :
            player.setDead()
            print(e)

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
        if (gameIsOver()):  print(GameOverException("endReached"))
    
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