class Referee(object):
    def clamp(int val, int min, int max):
        return max(min, min(max, val))


def  moveTo(x,y):
	currentPosition=self.position
	target=Case(x,y)
	if currentPosition.equals(targetPosition):self.action=SLOWER();return
	if self.speed==2:self.action=SLOWER()
	elif self.speed==1:
		#Suppose we've moved first
        currentPosition = currentPosition.neighbor(self.orientation)
        if (not currentPosition.valide()):self.action = SLOWER();break
        #Target reached at next turn
        if (currentPosition.equals(targetPosition)):self.action = None;break
        #For each neighbor cell, find the closest to target
        targetAngle = currentPosition.angle(targetPosition)
        angleStraight = min(abs(self.orientation - targetAngle), 6 - abs(self.orientation - targetAngle))
        anglePort = min(abs((self.orientation + 1) - targetAngle), abs((self.orientation - 5) - targetAngle))
        angleStarboard = min(abs((self.orientation + 5) - targetAngle), abs((self.orientation - 1) - targetAngle))

        centerAngle = currentPosition.angle(new Coord(MAP_WIDTH / 2, MAP_HEIGHT / 2))
        anglePortCenter = min(abs((self.orientation + 1) - centerAngle), abs((self.orientation - 5) - centerAngle))
        angleStarboardCenter = min(abs((self.orientation + 5) - centerAngle), abs((self.orientation - 1) - centerAngle))
        #Next to target with bad angle, slow down then rotate (avoid to turn around the target!)
        if (currentPosition.distanceTo(targetPosition) == 1 and angleStraight > 1.5):self.action = SLOWER();break

        distanceMin = None
        # Test forward
        nextPosition = currentPosition.neighbor(self.orientation)
        if (nextPosition.valide()):distanceMin = nextPosition.distanceTo(targetPosition);self.action =None
        #Test port
        nextPosition = currentPosition.neighbor((self.orientation + 1) % 6)
        if (nextPosition.valide()):
            distance = nextPosition.distanceTo(targetPosition)
            if (distanceMin == None or distance < distanceMin or distance == distanceMin and anglePort < angleStraight - 0.5):
                distanceMin = distance
                self.action = PORT()
        		break
        #Test starboard
        nextPosition = currentPosition.neighbor((self.orientation + 5) % 6)
        if (nextPosition.valide()):
            distance = nextPosition.distanceTo(targetPosition)
            if (distanceMin == None or distance < distanceMin
                    or (distance == distanceMin and angleStarboard < anglePort - 0.5 and self.action == Action.PORT)
                    or (distance == distanceMin and angleStarboard < angleStraight - 0.5 and self.action == None)
                    or (distance == distanceMin and self.action == Action.PORT and angleStarboard == anglePort
                            and angleStarboardCenter < anglePortCenter)
                    or (distance == distanceMin and self.action == Action.PORT and angleStarboard == anglePort
                            and angleStarboardCenter == anglePortCenter and (self.orientation == 1 or self.orientation == 4))):
                distanceMin = distance
                self.action = STARBOARD()
        		break
    elif self.speed==1:
    	#Rotate ship towards target
        targetAngle = currentPosition.angle(targetPosition)
        angleStraight = min(abs(self.orientation - targetAngle), 6 - abs(self.orientation - targetAngle))
        anglePort = min(abs((self.orientation + 1) - targetAngle), abs((self.orientation - 5) - targetAngle))
        angleStarboard = min(abs((self.orientation + 5) - targetAngle), abs((self.orientation - 1) - targetAngle))

        centerAngle = currentPosition.angle(new Coord(MAP_WIDTH / 2, MAP_HEIGHT / 2))
        anglePortCenter = min(abs((self.orientation + 1) - centerAngle), abs((self.orientation - 5) - centerAngle))
        angleStarboardCenter = min(abs((self.orientation + 5) - centerAngle), abs((self.orientation - 1) - centerAngle))
        forwardPosition = currentPosition.neighbor(self.orientation)
        self.action = None;

        if (anglePort <= angleStarboard):self.action = PORT()
      
        if (angleStarboard < anglePort or angleStarboard == anglePort and angleStarboardCenter < anglePortCenter
                or angleStarboard == anglePort and angleStarboardCenter == anglePortCenter and (self.orientation == 1 or self.orientation == 4)):self.action =STARBOARD()
    
        if (forwardPosition.valide() and angleStraight <= anglePort and angleStraight <= angleStarboard):self.action = FASTER()
        break
