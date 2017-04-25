# To debug: print >> sys.stderr, "Debug messages..."
import sys
import time

actions=''
def getObject(i,j):
    global objects
    return objects[hash(tuple([i,j]))]
class Entity(object):
    def __init__(self,x,y):
       self.x,self.y=x,y
class Bender(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.beer=0
         self.priority=1
         self.currentChar=' '
         self.direction=""
    def updateDirection(self):
        global actions
        global objects
        if self.priority:
            if  getObject(self.x,self.y+1).value!='#' and getObject(self.x,self.y+1).value!='X':self.y+=1;self.direction='SOUTH'
            elif getObject(self.x+1,self.y).value!='#' and getObject(self.x+1,self.y).value!='X':self.x+=1;self.direction='EAST'
            elif getObject(self.x,self.y-1).value!='#' and getObject(self.x,self.y-1).value!='X':self.y-=1;self.direction='NORTH'
            elif getObject(self.x-1,self.y).value!='#' and getObject(self.x-1,self.y).value!='X':self.x-=1;self.direction='WEST'
            else:0/0
        else:
            if getObject(self.x-1,self.y).value!='#' and getObject(self.x-1,self.y).value!='X':self.x-=1;self.direction='WEST'
            elif getObject(self.x,self.y-1).value!='#' and getObject(self.x,self.y-1).value!='X':self.y-=1;self.direction='NORTH'
            elif getObject(self.x+1,self.y).value!='#' and getObject(self.x+1,self.y).value!='X':self.x+=1;self.direction='EAST'
            elif getObject(self.x,self.y+1).value!='#' and getObject(self.x,self.y+1).value!='X':self.y+=1;self.direction='SOUTH'
            else:0/0
        actions+=self.direction+'\n'
    def displayDirection(self):
        global actions
        if self.direction=='WEST':
            if (getObject(self.x-1,self.y).value!='X' or self.beer) and getObject(self.x-1,self.y).value!='#':self.x-=1;actions+=self.direction+'\n'
            else:self.updateDirection()
        elif self.direction=='EAST':
            if (getObject(self.x+1,self.y).value!='X' or self.beer)and  getObject(self.x+1,self.y).value!='#':self.x+=1;actions+=self.direction+'\n'
            else:self.updateDirection()
        elif self.direction=='SOUTH':
            if(getObject(self.x,self.y+1).value!='X' or self.beer) and getObject(self.x,self.y+1).value!='#':self.y+=1;actions+=self.direction+'\n'
            else:self.updateDirection()
        elif self.direction=='NORTH':
            if (getObject(self.x,self.y-1).value!='X' or self.beer) and getObject(self.x,self.y-1).value!='#':self.y-=1;actions+=self.direction+'\n'
            else:self.updateDirection()
        else:0/0
        
        
class X(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.value='X'
    def collison(self,belder):
        if bender.beer:self.value=' '
        bender.displayDirection()
#Y is border
class Y(Entity):
     def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.value='#'
     def collison(self,belder):bender.displayDirection()
class NEWS(Entity):
     def __init__(self,x,y,a):
         Entity.__init__(self,x,y)
         if a=='E':self.value='EAST'
         elif a=='S':self.value='SOUTH'
         elif a=='N':self.value='NORTH'
         elif a=='W':self.value='WEST'
         else:0/0
     def collison(self,belder):
        bender.direction=self.value
        bender.displayDirection()
class Beer(Entity):
     def __init__(self,x,y):
         Entity.__init__(self,x,y) 
         self.value='B'
     def collison(self,belder):
        bender.beer=(bender.beer+1)%2
        bender.displayDirection()
#Dont change properties        
class I(Entity):
     def __init__(self,x,y):
         Entity.__init__(self,x,y)  
         self.value='I'
     def collison(self,belder):
        bender.priority=(bender.priority+1)%2
        bender.displayDirection()
class Blank(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.value=' '
    def collison(self,belder):bender.displayDirection()
class Suicide(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.value='$'
    def collison(self,belder):bender.currentChar='$'    
class Start(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.value='@'
         self.firtWalk=0
    def collison(self,belder):
        bender.displayDirection()    
class Teleporter(Entity):
    def __init__(self,x,y):
         Entity.__init__(self,x,y)
         self.twin=None
         self.value='T'
    def collison(self,belder):
        bender.x,bender.y=self.twin.x,self.twin.y
        bender.displayDirection()
l, c = [int(i) for i in raw_input().split()]
objects={}
bender=None
k=0
for i in xrange(l):
    tmp=[]
    s=raw_input()
    for j in range(len(s)):
        if s[j]=='#':o=Y(j,i)
        elif s[j]=='N' or s[j]=='W' or s[j]=='S' or s[j]=='E':o=NEWS(j,i,s[j])
        elif s[j]=='X':o=X(j,i)
        elif s[j]=='I':o=I(j,i)
        elif s[j]=='$':o=Suicide(j,i)
        elif s[j]=='T':
            o=Teleporter(j,i)
            if k==0:t1=o;k+=1
            else:o.twin=t1;t1.twin=o
        elif s[j]=='B':o=Beer(j,i)
        elif s[j]=='@':o=Start(j,i);bender=Bender(j,i)
        elif s[j]==' ':o=Blank(j,i)
        objects[hash(tuple([j,i]))]=o
t1=time.time()
TimeOut=False
bender.direction='SOUTH'
while bender.currentChar!='$' and not TimeOut:
    getObject(bender.x,bender.y).collison(bender)
    t2=time.time()
    if t2-t1>=0.1:TimeOut=True
if TimeOut:print "LOOP"
else:print(actions)
