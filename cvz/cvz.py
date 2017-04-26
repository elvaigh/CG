import sys
import math
import queue
# Save humans, destroy zombies!
h,w=9000,16000
zone=2000
speed=400
my_speed=1000
class Entity(object):
    def __init__(self,i,x,y):
        self.i,self.x,self.y=i,x,y
    def distanceTo(self,entity):
        return distance(self.x,self.y,entity.x,entity.y)
class Human(Entity):
    def __init__(self,i,x,y):
       Entity.__init__(self,i,x,y)
    
class Enemy(Entity):
    def __init__(self,i,x,y,distance,humans):
        Entity.__init__(self,i,x,y)
        self.distance=distance
        self.closest_human=self._compute_human(humans)
        self.next_x,self.next_y=self._compute_position()
    def __str__(self):
        return str(self.i)
    def _compute_human(self,humans):
        closest_human,closest_dist=None,None
        for d in humans:
            dist=self.distanceTo(d)
            if closest_dist==None or closest_dist>dist:
                closest_human,closest_dist=d,dist
        return closest_human
    def _compute_position(self):    
        v=(self.closest_human.x-self.x,self.closest_human.y-self.y)
        dist=self.closest_human.distanceTo(self)
        if dist<=speed:
            return self.closest_human.x,self.closest_human.y
        else:
            c=speed/dist
            vect=c*v[0],c*v[1]
            return int(self.x+vect[0]),int(self.y+vect[1])
def distance(x,y,a,b):
    return math.sqrt((x-a)**2+(y-b)**2)
def valide(x,y):return x>-1 and x<9000 and y>-1 and y<16000
# class Strategy(object):
def bfs(sx, sy):
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
        if (stackConut > 500):break
        if (valide(cx, cy)):
            if ( curScore<gameGrid[cx][cy]):curScore=gameGrid[cx][cy];target=[cx,cy]
            nx,ny=cx+my_speed,cy+my_speed
            if valide(nx, ny):q.put((nx, ny))
            nx,ny=cx-my_speed,cy+my_speed
            if valide(nx, ny):q.put((nx, ny))
            nx,ny=cx+my_speed,cy-my_speed
            if valide(nx, ny):q.put((nx, ny))
            nx,ny=cx-my_speed,cy-my_speed
            if valide(nx, ny):q.put((nx, ny))
            v[cx][cy] = True
        #print("Debug messages...",curScore,stackConut,cur,target, file=sys.stderr)
    return None    

# game loop
human_count0=0
k=0
while True:
    gameGrid = [[0 for i in range(9000)] for j in range(16000)]
    x, y = [int(i) for i in input().split()]
    
    humans=[]
    enemies=[]
    dist=None
    human_count = int(input())
    if k==0:
        human_count0=human_count
        k+=1
    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]
        gameGrid[human_x][human_y]=100000
        if dist==None or dist>distance(x,y,human_x, human_y):
            dist=distance(x,y,human_x, human_y)
            a,b=human_x, human_y
        humans.append(Human(human_id, human_x, human_y))
    zombie_count = int(input())
    target=None
    dist=None
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]
        gameGrid[zombie_id][zombie_y]=10*human_count
        e=Enemy(zombie_id, zombie_xnext, zombie_ynext,distance(x,y,zombie_x, zombie_y),humans)
        enemies.append(e)
        if dist==None or dist>distance(x,y,zombie_xnext, zombie_ynext):
            dist=distance(x,y,zombie_xnext, zombie_ynext)
            target=e
    dist=None
    
    for i in enemies:
        if i.distanceTo(i.closest_human)>my_speed and (dist==None or dist>distance(x,y,i.closest_human.x,i.closest_human.y)):
            dist=distance(x,y,i.closest_human.x,i.closest_human.y)
            a,b=i.closest_human.x,i.closest_human.y
    if e and e.distanceTo(e.closest_human)<5*my_speed:a,b=e.x,e.y
    if human_count0==4:
        a,b=human_x, human_y
    
    print(bfs(x,y))
        # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Your destination coordinates
    
