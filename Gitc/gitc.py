import sys
import math
from collections import defaultdict
import time
# To debug: print("Debug messages...", file=sys.stderr)
class Entity(object):
    def __init__(self,entityId,arg1,arg2,arg3,arg4,arg5):
       self.entityId,self.arg1,self.arg2,self.arg3,self.arg4,self.arg5=entityId,arg1,arg2,arg3,arg4,arg5 
    def updateHistory(self,arg1,arg2,arg3,arg4,arg5):
       self.arg10,self.arg20,self.arg30,self.arg40,self.arg50=arg1,arg2,arg3,arg4,arg5 
        
class FACTORY(Entity):
     def __init__(self,entityId,arg1,arg2,arg3,arg4,arg5):
       Entity.__init__(self,entityId,arg1,arg2,arg3,arg4,arg5)
       self.entityType,self.links='FACTORY',[] 
       self.updateHistory(0,0,-1,0,0)
     def __str__(self):
         return "ID : "+str(self.entityId)+"Owner : "+str(self.arg1)
     def buildLink(self,factory,distance):self.links.append([factory,distance])
     def computeDistance(self,j):
         for i in self.links:
             if i[0].entityId==j.entityId:return i[1]
         return None
     def nearestFactory(self,player):
         x,d=None,100
         for j in self.links:
             if j[1]<d and j[0].arg1==player:x,d=j[0],j[1]
         return x,d
     def computeBestNeighbour(self):
        x,d,prod=None,1000,-1
        tmp=[]
        for j in self.links:
            if j[0].arg1==0 and j[0].arg3>prod:prod=j[0].arg3
        for j in self.links:
            if j[0].arg1==0 and j[0].arg3==prod :tmp.append([j[0],j[1]])
        for i in tmp:
            if i[1]<d :x,d=i[0],i[1]
        return x,d
     def nearestOfWith(self,troop,player):
        x,d=None,25
        for j in self.links:
            if j[1]<d and j[0].arg2>troop and j[0].arg1==player:d,x=j[1],j[0]
        return x,d
     def othersTargeted(self,troops,d):
        s=0
        for i in troops:
            if i.arg3==self.entityId and i.arg5<=d:s+=(i.arg1*i.arg4)
        return s
     def actionInDTurn(self,d):
        incs=int((self.arg2+d*self.arg3)/10)
        actions=[]
        if incs>0 and self.arg3<3:actions.extend(["INC "+str(self.entityId)+""])
        total=self.arg2+self.arg3*d
        for i in self.links:
            if i[1]<=d and total>i[0].arg2 +i[1]*i[0].arg3:
                actions.extend(["MOVE "+str(self.entityId)+" "+str(i[0].entityId)+" "+str(i[0].arg2 +i[1]*i[0].arg3)])
                total-=(i[0].arg2 +i[1]*i[0].arg3)
        return actions
     def routeTroop(self,arene):
         moves=""
         for i in arene.troops:
             if i.arg5==1 and i.arg3==self.entityId and i.arg1==self.arg1 and self.arg1==1 and i.targeted!=self.entityId:
                 moves+="MOVE"+str(self.entityId)+" "+str(i.targeted)+" "+str(i.arg4)+";"
         return moves
     def hasInc(self):
        return self.arg30<self.arg3 and self.arg30>=0
     def hasSentTroop(self,troops):
        sent=0
        for i in troops:
            if i.arg2==self.entityId and i.arg50-i.arg5==1:sent+=i.arg4
        return sent
            
class TROOP(Entity):
     def __init__(self,entityId,arg1,arg2,arg3,arg4,arg5):
       Entity.__init__(self,entityId,arg1,arg2,arg3,arg4,arg5)
       self.entityType='TROOP'
       self.targeted=None
       self.updateHistory(0,0,0,0,0)
class BOMB(Entity):
     def __init__(self,entityId,arg1,arg2,arg3,arg4,arg5):
       Entity.__init__(self,entityId,arg1,arg2,arg3,arg4,arg5)
       if self.arg1==-1:self.arg4=0
       self.entityType='BOMB'
     def getPosition(self):return self.arg4
     def setPosition(self,i):self.arg4+=1
     def nearestHarmfullFactory(self,facotories):
         if self.arg1==-1:
            for i in factories:
                d=factories[self.arg2].computeDistance(i)
                if i.arg1==1 and d and d-self.getPosition()==2:return i
         return None
class Player(object):
    def __init__(self,ID):
        self.ID,self.factories,self.troops,self.bombs,self.nbBombs,self.targeted,self.InitCyborgs=ID,[],[],[],0,[],0
        self.newattacked=None
        self.lastPicker=None
        self.modulus=0
    def getTroop(self):return self.troops
    def getFactories(self):return self.factories
    def getBombs(self):return self.bombs
    def setTroops(self,troops):
        tmp=[]
        for i in troops:
            if i.arg1==self.ID:tmp.extend([i])
        self.troops=tmp
    def setFactories(self,factories):
        tmp=[]
        for i in factories:
            if i.arg1==self.ID:tmp.extend([i])
        if len(self.factories)==0 and len(tmp)>0:self.InitCyborgs=tmp[0].arg2
        self.factories=tmp
    def setBooms(self,bombs):
        tmp=[]
        for i in bombs:
            if i.arg1==self.ID:tmp.extend([i])
        self.bombs=tmp
    def setNbBombs(self,nb):self.nbBombs=nb
    def computeMyTotal(self):
        s=0
        for i in factories:s+=i.arg2
        return s
    def computeMaxFactory(self):
        m,j=-1,None
        for i in self.factories:
            if i.arg2>m:m,j=i.arg2,i
        return j,m
    def computeMinFactory(self):
        m=401*15*3
        for i in self.factories:
            if i.arg2<m:m,j=i.arg2,i
        return j,m
    def computeMaxFactoryMaxPord(self):
        prod,j=-1,None
        for i in self.factories:
            if i.arg3>prod:prod,j=i.arg3,i
        return j
    def computeMinFactoryMinProd(self):
        m,prod=401*15*3,4
        for i in self.factories:
            if i.arg2<m and i.arg3<m:m,prod,j=i.arg2,i.arg3,i
        return j,m
    def prod(self):
        s=0
        for i in self.factories:s+=i.arg3
        return s  
    def maxTroop(self,arene):
        m=0
        for j in arene.troops:
            if j.arg4>m:m=j.arg4
        return m
    def minTroop(self):
        m=401*3*15
        for j in self.troops:
            if j.arg4<m:m=j.arg4
        return m
    def score(self):
        s=0
        for i in self.factories:
            s+=i.arg2
        return s
    def sendBombToPlayer(self,arene):
        player=arene.players[-1]
        target=player.computeMaxFactoryMaxPord()
        if len(player.factories )==1:
            target=player.factories[0]
        source=None
        if target:
            source,d=target.nearestFactory(self.ID)
        if source and (target.arg3>=2  or arene.turn==1) and len(self.targeted)<2 and target.entityId not in self.targeted:
            self.targeted.extend([target.entityId])
            return "BOMB "+str(source.entityId)+" "+str(target.entityId)+";"
        return ""
    def sendTroop(self,source,dest,nbTroop,arene):
        dists,paths=arene.allDijsktra[source.entityId]
        pathsKeys=list(paths)
        finalDest=dest.entityId
        dest1=finalDest
        while finalDest!=source.entityId:
            dest1,finalDest=finalDest,paths[finalDest]
        if arene.factories[dest1].arg1==self.ID:pass
        else:dest1=dest.entityId
        return "MOVE "+str(source.entityId)+" "+str(dest1)+" "+str(nbTroop)+";"
    def hasActivetedBomb(self):return len(self.bombs)>0
    def routeALL(self,arene):
        s=""
        for i in self.factories:
            s+=i.routeTroop(arene)
        return s
    def increaseProd(self,arene):
        moves=""
        for i in self.factories:
            d=int((i.arg2-10)/(1+i.arg3))+1
            s=i.othersTargeted(arene.getTroops(),d)
            if i.arg2>=10 and i.arg3<3:moves+="INC "+str(i.entityId)+";"
        return moves
    
    def AttackedFactoryBy(self,player):
        attacked=[]
        for i in player.troops:
            for j in self.factories:
                if i.arg3 == j.arg3:attacked.append([j,i.arg4,i.arg5])
        return attacked
    def pickUpFactory(self,arene):
        moves=""
        for i in self.factories:
            b,d=i.computeBestNeighbour()
            if b and b.arg2<i.arg2:moves+=self.sendTroop(i,b,b.arg2+1,arene)
        return moves
    
       
    def attackWithTurnProd(self,arene):
        moves=""
        
        for j in self.factories:
            t,d=j.nearestFactory(-1)
            if arene.turn%(arene.factory_count) ==0:
                nbTroop=abs(self.score()-arene.players[-1].score())+1#self.minTroop()
            else:
                nbTroop=j.arg3*j.arg2
            if t:moves+=self.sendTroop(j,t,nbTroop,arene)
        return moves
    def attackFactories(self,arene):
        moves=""
        mainFactory,m=self.computeMaxFactory()
        fact,m=arene.players[-1].computeMaxFactory()
        if mainFactory and fact and self.hasActivetedBomb():moves= "MOVE "+str(mainFactory.entityId)+" "+str(fact.entityId)+" "+str(3)+";"
        return moves
    def defend(self,arene):
        moves=""
        j=0
        for i in self.factories:
            defender,d=i.nearestFactory(1)
            if defender and self.AttackedFactoryBy(arene.players[-1]):
                
                moves+=self.sendTroop(defender,i,10,arene)#à amelier
        return moves
        
    def liveFactory(self,factory,arene):
        n0,d=factory.nearestFactory(1)#à amelier
        if not n0 or factory.arg1!=1:
            n0,d=factory.computeBestNeighbour()
            if not n0 or factory.arg1!=1:return ""
            return self.sendTroop(factory,n0,factory.arg2,arene)
        return self.sendTroop(factory,n0,factory.arg2,arene)
    def avoidBombs(self,player,arene):
        if player.hasActivetedBomb():
            for i in player.bombs:
                ne=i.nearestHarmfullFactory(arene.factories)
                if ne :return self.liveFactory(ne,arene)
        return ""
    def factoriesActions(self):
        d=1
        for i in self.factories:print("Actions for : ",i.entityId," are : ",i.actionInDTurn(d), file=sys.stderr)
    def displayActions(self,troops):
        for i in self.factories:
            sent=i.hasSentTroop(troops)
            #if i.hasInc():print("Increase factory : ",i.entityId," By",i.arg3-i.arg30,file=sys.stderr)
            if sent>0: print("Factory : ",i.entityId," Sent",sent,file=sys.stderr)
            #print("Factory : ",i.entityId,"arg2 : ",i.arg2, " :",i.arg20,"arg3 : ",i.arg3,":",i.arg30,file=sys.stderr)
    def playerLoop(self,player,arene):
        # self.factoriesActions()
        moves=""
        if arene.turn==1:
            self.modulus=self.factories[0].entityId%2
        prodMSG="MSG ma prod : "+str(self.prod())+"  Ta prod ; "+str(player.prod())
        if arene.turn<=int(arene.factory_count/2):
            # moves+=self.defend(arene)
            moves+=self.attackFactories(arene)
            moves+=self.increaseProd(arene)
            moves+=self.pickUpFactory(arene)
            moves+=self.sendBombToPlayer(arene)
        else:
            moves+=self.increaseProd(arene)
            moves+=self.pickUpFactory(arene)
            moves+=self.attackWithTurnProd(arene)
            moves+=self.sendBombToPlayer(arene)
            moves+=self.attackFactories(arene)
            moves+=self.avoidBombs(player,arene)
            # moves+=self.defend(arene)
        if len(moves)>0:return moves+prodMSG
        return "WAIT"
            
class Arene(object):
    def __init__(self):
        self.players,self.noOneFactories,self.troops,self.factories=[],[],[],[]
        self.turn=0
        self.historyTroops=[]
        self.links=None
        self.allDijsktra=[]
        self.factory_count=0
    def getNoOneFactories(self):return self.noOneFactories
    def getTroops(self):return self.troops
    def setPlayers(self,player):self.players=players
    def setTroops(self,troops):self.troops=troops
    def setNoOneFactories(self,factories):
        self.noOneFactories=[]
        for i in factories:
            if i.arg1==0:self.noOneFactories.extend([i])
    def updateLinks(self):
        for i in self.factories:
            for j in i.links:
                for k in self.factories:
                    if j[0].entityId==k.entityId:j[0]=k
class Graph:
  def __init__(self):
    self.nodes = set()
    self.edges = defaultdict(list)
    self.distances = {}
    

  def add_node(self, value):
    self.nodes.add(value)

  def add_edge(self, from_node, to_node, distance):
    self.edges[from_node].append(to_node)
    self.edges[to_node].append(from_node)
    self.distances[(from_node, to_node)] = distance


def dijsktra(graph, initial):
  visited = {initial: 0}
  path = {}

  nodes = set(graph.nodes)

  while nodes: 
    min_node = None
    for node in nodes:
      if node in visited:
        if min_node is None:
          min_node = node
        elif visited[node] < visited[min_node]:
          min_node = node

    if min_node is None:
      break

    nodes.remove(min_node)
    current_weight = visited[min_node]

    for edge in graph.edges[min_node]:
      weight = current_weight + graph.distances[(min_node, edge)]
      if edge not in visited or weight < visited[edge]:
        visited[edge] = weight
        path[edge] = min_node
  return visited, path       
  
  
  
tmps1=time.time()         
firstTurn=0         

players=[Player(1),Player(-1)]
gameArene=Arene()

factories=[]
factory_count = int(input())  # the number of factories
for i in range(factory_count):
    factories.extend([FACTORY(i,0,0,0,0,0)])

link_count = int(input())  # the number of links between factories
links=[]
myGraph=Graph()
for i in range(factory_count):
    myGraph.add_node(i)
for i in range(link_count):
    factory_1, factory_2, distance = [int(j) for j in input().split()]
    factories[factory_1].buildLink(factories[factory_2],distance)
    factories[factory_2].buildLink(factories[factory_1],distance)
    print("distances ",factory_1,factory_2,distance,file=sys.stderr)
    myGraph.add_edge(factory_1,factory_2,distance)
    myGraph.add_edge(factory_2,factory_1,distance)
    key=[factory_1,factory_2,distance]
    links.append(key)
for i in range(factory_count):
    gameArene.allDijsktra.extend([dijsktra(myGraph,i)])
gameArene.factory_count=factory_count
tmps2=time.time()            
bombs=[]
troops=[]
historyTroop={}
historyTroop[0]=[]
initial=0
while True:
    troops=[]
    tmps3=time.time()
    entity_count = int(input())  # the number of entities (e.g. factories and troops)
    for i in range(entity_count):
     entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
     entity_id,arg_1,arg_2,arg_3,arg_4,arg_5 = int(entity_id),int(arg_1),int(arg_2),int(arg_3),int(arg_4),int(arg_5)
     if entity_type=='FACTORY':
           factories[entity_id].arg1,factories[entity_id].arg2,factories[entity_id].arg3,factories[entity_id].arg4= arg_1, arg_2, arg_3,arg_4
     elif entity_type=="TROOP":
        b=TROOP(entity_id,arg_1, arg_2, arg_3, arg_4, arg_5)
        troops.extend([b]) 
     elif entity_type=="BOMB":
         find=False
         for i in bombs:
             if i.entityId==entity_id:
                 if i.arg1==-1: i.setPosition(i.getPosition()+1)
                 else:i.arg4=arg_4
                 find=True
         if not find:b=bombs.extend([BOMB(entity_id,arg_1, arg_2, arg_3, arg_4, arg_5)])
    gameArene.turn+=1
    for i in players:
        i.setTroops(troops)
        i.setFactories(factories)
        i.setBooms(bombs)
    gameArene.setTroops(troops)
    gameArene.setNoOneFactories(factories)
    gameArene.setPlayers(players)
    gameArene.factories=factories
    gameArene.updateLinks()
    
    print(players[0].playerLoop(players[1],gameArene))
    
    tmps4=time.time()
    if gameArene.turn==1:print("First time : ",tmps2-tmps1,"Loop time",tmps4-tmps3,file=sys.stderr)
   
