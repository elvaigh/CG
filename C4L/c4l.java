import java.util.*;
import java.io.*;
import java.math.*;
// To debug: System.err.println("Debug messages...");
enum MoleculeType {
		A, B, C, D, E;
}
enum Module {
	SAMPLES, DIAGNOSIS, MOLECULES, LABORATORY, START_POS;	
}
class PlayerData {
	int[] storage, expertise,need;
	boolean dead, attemptConnection, moved;
	int eta, score, deadAt, index,diagnosis,curNeed,samples,attente;
	String [] molecules;
	String message, connectionData;
	String action;
	Sample tobe;
	Sample[] diagnotics;
	Module from, target;
	public PlayerData(int index) {
	    attente=0;
		from = Module.START_POS;
		target = Module.START_POS;
		eta = 0;
		storage = new int[5];
		expertise = new int[5];
		need=new int[5] ;
		diagnotics=new Sample[3];
		this.molecules=new String[5]; 
		for(int i=0;i<5;i++){
		    need[i]=0;   
		}
		this.molecules[0]="A";
		this.molecules[1]="B";
		this.molecules[2]="C";
		this.molecules[3]="D";
		this.molecules[4]="E";
		this.index = index;
		score = 0;
		diagnosis=0;
		tobe=null;
		samples=0;
	}
    public void update(Module target,int eta, int score,int[] storage, int [] expertise){
        this.from=this.target;
        this.target=target;   
        this.eta=eta;
        this.score=score;
        this.storage=storage;
        this.expertise=expertise;
        samples=0;
    }
	public void play(){
	    System.err.println("mon attente"+attente);
	    if(eta>0){
	        action="WAIT";
	        return;
	    }
	    if(target==Module.START_POS || (from==Module.LABORATORY && samples==0)){
	        action="GOTO SAMPLES";
	    }
	    else if(target==Module.SAMPLES ){
	        if(samples<3){
	            int i=(int)(1.2+Math.random()+Player.turn/200.0);
	            int s=countMolecules(expertise);
	            if(s<5)i=1;
	            else if(s<10)i=2;
	            else i=3;
	           // if(i>3)i=3;
	            action="CONNECT "+i;
	        }else{
	            action="GOTO DIAGNOSIS";
	        }
	    }
	    else if(target==Module.DIAGNOSIS){
	       
	       for(Sample ss:Player.mySamples){
	           if(ss!=null && ss.life<0){
	             action="CONNECT "+ss.id;
	             return ;
	           }
	       }
	       
	       for(Sample ss:Player.mySamples){
    	       if(ss!=null & enoughExpertise(ss)){
    	           tobe=ss;
    	            action="GOTO LABORATORY";
    	            return;
    	        }
	       }
    	   
	       for(Sample ss:Player.mySamples){
	           if(ss!=null && ss.life>0 && !canBeTreated(ss)){
	             action="CONNECT "+ss.id;
	             return ;
	           }
	       }
    	      
	       System.err.println("samples "+samples);
	       if(samples>0){
	           action="GOTO MOLECULES";
	           return;
	       }
	       if(samples==0){
	           action="GOTO SAMPLES";
	           return;
	       }
	       
	    }
	    else if(target==Module.MOLECULES){
	        if(tobe==null){
	            tobe=myBest();
	        }
	        curNeed=0;
	        if(tobe==null){
	            if(samples<3){
    	            action="GOTO SAMPLES";
    	        }else{
    	            action="WAIT";
    	        }
	             return;
	        }
	       
	        System.err.println(tobe);
	        //curNeed=fillMolecule();
	        curNeed=FindBiggest(storage,expertise);
	        
	        if(curNeed<5 && tobe.cost[curNeed]>storage[curNeed]+expertise[curNeed] ){
	            if(Player.availables[curNeed]>0 && countMolecules(storage)<10)action="CONNECT "+molecules[curNeed];
	            else{
	                 action="WAIT";
	            }
	        }else{
	        	int cc=countMolecules(storage)+countMolecules(expertise)-countMolecules(tobe.cost);
	           if(cc>=0)action="GOTO LABORATORY";
	           else{ 
	                action="WAIT"; 
	           }
	        }
	        
	    }
	    else if(target==Module.LABORATORY){
	        
	        for(Sample ss:Player.mySamples){
    	       if(ss!=null & enoughExpertise(ss)){
    	            action="CONNECT "+ss.id;
	                tobe=null;
	                return;
    	        }
	        }
            if(samples>0){
                action="GOTO MOLECULES";
            }else{
                diagnosis=0;
                action="GOTO SAMPLES";
            }
	        
	    }
	    
	}
	
	public  int FindSmallest(int [] arr1,int [] arr2){//start method

       int index = 0;
       int min = arr1[index]+arr2[index];
       for (int i=1; i<arr1.length; i++){

           if (arr1[i]+arr2[i] < min ){
               min = arr1[i]+arr2[i];
               index = i;
           }


       }
       return index ;

	}
	public  int FindBiggest (int [] arr1,int [] arr2){//start method

       int index = 0;
       int min = arr1[index]+arr2[index];
       for (int i=1; i<arr1.length; i++){

           if (arr1[i]+arr2[i] > min  && tobe[i]>arr1[i]+arr2[i]){
               min = arr1[i]+arr2[i];
               index = i;
           }


       }
       return index ;

	}
	public boolean notGood(Sample tobe){
	    for(int i=0;i<5;i++){
	        if(expertise[i]+Player.availables[i]+storage[i]<tobe.cost[i])return false;
	    }
	    return true;
	}
	public boolean enoughExpertise(Sample tobe){
	    if(tobe==null)return false;
	    for(int i=0;i<5;i++){
	        if(expertise[i]+storage[i]< tobe.cost[i])return false;
	    }
	    return true;
	}
	public boolean canBeTreated(Sample s){
	    for(int i=0;i<5;i++){
	      if(s.cost[i]>Player.availables[i]+expertise[i]+storage[i])return false;
	    }
	    return true;
	}
	int cost(Sample s){
	    int t=0;
	    if(s==null)return 1;
	    for(int i=0;i<5;i++){
	        t+=s.cost[i];
	    }
	    return t;
	}
	public Sample myBest(){
	     int h=100,c;
	     Sample tmp=null;
         for(Sample s:Player.mySamples){
            
             if(s!=null && s.life<h &&  canBeTreated(s)){
                 h=s.life;
                 tmp=s;
             }
         }
         return tmp;
	}
	public int countMolecules(int t[]){
	    int s=0;
	    for(int i=0;i<5;i++){
	     s+=t[i];   
	    }
	    return s;
	}
	
	

	public boolean isMoving() {
		return eta > 0;
	}
}
class Sample {
	public static int ENTITY_COUNT = 0;
	String expertise;
	int life;
	int[] cost;
	int id, rank;
	private boolean discovered=false;
	PlayerData discoveredBy;
    public void update(int[] cost, int life, String gain) {
		this.expertise = gain;
		this.life = life;
		this.cost = cost;
	}
	public Sample(int id,int rank) {
	    this.id=id;
	    this.rank=rank;
	    this.cost=new int[5];
	}
	public void setDiscovered(boolean discovered) {
		this.discovered = discovered;

	}
	public boolean isDiscovered() {
		return discovered;

	}
	public Sample clone() {
		Sample tmp= new Sample(this.id,this.rank);
		tmp.update(this.cost, this.life, this.expertise);
		return tmp;
	}
	
}
class ScienceProject {
	int[] cost;
	int index;
	public ScienceProject(int id,int[] cost) {
	    this.index=id;
		this.cost = cost;
	}
}

class Player {
    static int turn=0;
    static ScienceProject[] projetcs;
    static PlayerData[] players=new PlayerData[2];
    static Sample[] cloud;
    static int maxCloudSaples=50;
    static Sample[] mySamples;
    static int[] availables=new int[5];
    
    public static void main(String args[]) {
        players[0]=new PlayerData(0);
        players[1]=new PlayerData(1);
        
        Scanner in = new Scanner(System.in);
        int projectCount = in.nextInt();
        projetcs=new ScienceProject[projectCount];
        for (int i = 0; i < projectCount; i++) {
            int a = in.nextInt();
            int b = in.nextInt();
            int c = in.nextInt();
            int d = in.nextInt();
            int e = in.nextInt();
            projetcs[i]=new ScienceProject(i,new int[] {a,b,c,d,e});   

        }
        // game loop
        while (true) {
            cloud=new Sample[maxCloudSaples];
            mySamples=new Sample[3];
            int j=0;
            for (int i = 0; i < 2; i++) {
                String target = in.next();
                int eta = in.nextInt();
                int score = in.nextInt();
                int storageA = in.nextInt();
                int storageB = in.nextInt();
                int storageC = in.nextInt();
                int storageD = in.nextInt();
                int storageE = in.nextInt();
                int expertiseA = in.nextInt();
                int expertiseB = in.nextInt();
                int expertiseC = in.nextInt();
                int expertiseD = in.nextInt();
                int expertiseE = in.nextInt();
                players[i].update(Module.valueOf(target),eta,score,new int[] {storageA,storageB,storageC,storageD,storageE},new int[] {expertiseA,expertiseB,expertiseC,expertiseD,expertiseE});
            }
            int availableA = in.nextInt();
            int availableB = in.nextInt();
            int availableC = in.nextInt();
            int availableD = in.nextInt();
            int availableE = in.nextInt();
            availables=new int[] {availableA,availableB,availableC,availableD,availableE};
            int sampleCount = in.nextInt();            
            for (int i = 0; i < sampleCount; i++) {
                int sampleId = in.nextInt();
                int carriedBy = in.nextInt();
                int rank = in.nextInt();
                String expertiseGain = in.next();
                int health = in.nextInt();
                int costA = in.nextInt();
                int costB = in.nextInt();
                int costC = in.nextInt();
                int costD = in.nextInt();
                int costE = in.nextInt();
                System.err.println("Message "+carriedBy);
                if(carriedBy==0){
                    mySamples[j]=new Sample(sampleId,rank);
                    players[carriedBy].samples=j+1;
                    mySamples[j].update(new int[] {costA,costB,costC,costD,costE},health,expertiseGain);
                    j++;
                }
            }    
            players[0].play();
            System.out.println(players[0].action);
            turn++;
            //System.out.println("WAIT");
        }
    }
}