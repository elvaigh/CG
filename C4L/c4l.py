import sys
import math
# To debug: print("Debug messages...", file=sys.stderr)
MAX_SAMPLE=3
MAX_MOLECULE=10
class Sample(object):
    def __init__(self,entityId):
       self.entityId=entityId
       self.rank,self.gain,self.health,self.costA,self.costB,self.costC,self.costD,self.costE=0,0,0,0,0,0,0,0
    def update(self,rank,gain,health,costA,costB,costC,costD,costE):
        self.rank,self.gain,self.health,self.costA,self.costB,self.costC,self.costD,self.costE=rank,gain,health,costA,costB,costC,costD,costE
        
class Bot(object):
    def __init__(self,entityId):
        self.entityId=entityId
        self.carried=0
        self.carriedSamples=[]
        self.finished=False
        self.rnk=0
    def update(self,target,eta,storageA, storageB, storageC, storageD, storageE,expertiseA, expertiseB, expertiseC, expertiseD, expertiseE):
        self.target,self.eta,self.storageA,self.storageB,self.storageC,self.storageD,self.storageE,expertiseA,self.expertiseB,self.expertiseC,self.expertiseD,self.expertiseE=target,eta,storageA, storageB, storageC, storageD, storageE,expertiseA, expertiseB, expertiseC, expertiseD, expertiseE
    def loadSamples(self,cloud):
        health=-1
        tmp=None
        for i in cloud:
            if i.rank>health:health=i.rank;tmp=i
        return tmp.rank
    def play(self,simples,cloud):
        global mysamples
        if self.eta!=0:print("WAIT");return
        if self.target=="START_POS" or (self.target=="LABORATORY" and not self.finished):print("GOTO SAMPLES")
        elif self.target=="SAMPLES"  and self.rnk==0:
            # rk=self.loadSamples(cloud)
            self.rnk+=1
            print("CONNECT",1)
        elif self.target=="SAMPLES"  and self.rnk==1:self.carriedSamples=simples;print("GOTO DIAGNOSIS");self.rnk=0
        elif self.target=="DIAGNOSIS" and self.carried<1:
            self.carried+=1
            self.carriedSamples=simples
            print("CONNECT",self.carriedSamples[0].entityId)
        elif self.target=="DIAGNOSIS":print("GOTO MOLECULES")
        elif self.target=="MOLECULES":
            print("storagees...",self.storageA,self.carriedSamples[0].costA, file=sys.stderr)
            if self.storageA<self.carriedSamples[0].costA:print("CONNECT A")
            elif self.storageB<self.carriedSamples[0].costB:print("CONNECT B")
            elif self.storageC<self.carriedSamples[0].costC:print("CONNECT C")
            elif self.storageD<self.carriedSamples[0].costD:print("CONNECT D")
            elif self.storageE<self.carriedSamples[0].costE:print("CONNECT E")
            else:print("GOTO LABORATORY");self.finished=True
        elif self.target=="LABORATORY" and self.finished:
            print("CONNECT",self.carriedSamples[0].entityId)
            self.carriedSamples=[]
            self.carried=0
            self.finished=False
            mysamples=[]
        else:print("lallalaalla")
project_count = int(input())
# print("Debug messages...",project_count, file=sys.stderr)
for i in range(project_count):
    a, b, c, d, e = [int(j) for j in input().split()]
j=0
bots=[Bot(0),Bot(1)]
mysamples=[]
# game loop
while True:
    
    cloud=[]
    enemysamples=[]
    for i in range(2):
        target, eta, score, storage_a, storage_b, storage_c, storage_d, storage_e, expertise_a, expertise_b, expertise_c, expertise_d, expertise_e = input().split()
        bots[i].update(target,int(eta),int(storage_a),int(storage_b),int(storage_c),int(storage_d),int(storage_e),int(expertise_a),int(expertise_b),int(expertise_c),int(expertise_d),int(expertise_e))
    available_a, available_b, available_c, available_d, available_e = [int(i) for i in input().split()]
    sample_count = int(input())
    for i in range(sample_count):
        sample_id, carried_by, rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e =input().split()
        sample_id=int(sample_id)
        carried_by=int(carried_by)
        rank=int(rank)
        health, cost_a, cost_b, cost_c, cost_d, cost_e=int(health), int(cost_a), int(cost_b), int(cost_c),int(cost_d), int(cost_e)
        
        if carried_by==0 :
            if len(mysamples)==0:mysamples+=[Sample(sample_id)]  
            else:mysamples[0].update(rank, expertise_gain, health, cost_a, cost_b, cost_c, cost_d, cost_e)
        elif carried_by==1:enemysamples+=[Sample(sample_id)] 
        else:cloud+=[Sample(sample_id)] 
    print("Debug cost",len(cloud), file=sys.stderr)
    bots[0].play(mysamples,cloud)
    # print("WAIT")