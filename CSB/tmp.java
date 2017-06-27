import java.util.*;
import java.io.*;
import java.math.*;

// To debug: System.err.println("Debug messages...");
class Point{
     double x,y,sx,sy;
     public Point(double x,double y){
      this.x=x;
      this.y=y;
     }
     public double distance2(double x,double y){
      double dx=(x-this.x);
      double dy=(y-this.y);
      return dx*dx+dy*dy;
    }
     public double distance2(Point p){
          double  dx=(p.x-this.x);
          double dy=(p.y-this.y);
          return dx*dx+dy*dy;
     }
     public double distance(Point p){return (double)Math.sqrt(distance2(p));}
     public double distance(double x,double y){return (double)Math.sqrt(distance2(x,y));}
     double getAngle(Point p) {
	    double d = distance(p);
	    double dx = (p.x - x) / d;
	    double dy = (p.y - y) / d;

	    // Simple trigonometry. We multiply by 180 / Math.PI to convert radiants to degrees.
	    double a = (double)Math.acos(dx) * 180 / (double)Math.PI;

	    // If the point I want is below me, I have to shift the angle for it to be correct
	    if (dy < 0) {
	        a = (double)(360 - a);
	    }

	    return a;
	}
	 Point closest(Point a, Point b) {
	    double da = b.y - a.y;
	    double db = a.x - b.x;
	    double c1 = da*a.x + db*a.y;
	    double c2 = -db*x + da*y;
	    double det = da*da + db*db;
	    double cx = 0;
	    double cy = 0;

	    if (det != 0) {
	        cx = (da*c1 - db*c2) / det;
	        cy = (da*c2 + db*c1) / det;
	    } else {
	        // The point is already on the line
	        cx = x;
	        cy = y;
	    }

	    return new Point(cx, cy);
	}
//  public void load(){this.x=this.sx;this.y=this.sy;}
//  public void store(){this.sx=this.x;this.sy=this.y;}
}
class Unit extends Point{

    
}
class CheckPoint extends Unit{
 int id,r;
 public CheckPoint(double x,double y,int id){super(x,y);this.id=id;this.r=600;}
 void collision(Pod p){p.timeout=100;p.checked++;}
}
class Pod extends Unit{
    int checked,schecked,shieldcount,sshieldcount,nextCheckPointId,snextCheckPointId,timeout,stimeout,r,thrust,sthrust;
    double vx,vy,svx,svy,angle,sangle,lastVx,lastVy;
    boolean shield;
    public Pod(double x,double y,double vx,double vy,double angle,int nextCheckPointId){
        super(x,y);this.timeout=100;this.thrust=100;
        this.vx=vx;this.vy=vy;this.angle=angle;this.r=400;this.nextCheckPointId=nextCheckPointId;
        this.shield=false;
        lastVx=0;
        lastVy=0;
        shieldcount=3;
    }
    void  update(double x,double y,double vx,double vy,double angle,int nextCheckPointId){
        this.x=x;this.y=y;
        lastVx=vx;lastVx=vy;
        this.vx=vx;this.vy=vy;this.angle=angle;this.nextCheckPointId=nextCheckPointId;
    }
    void store(){
        sx=x;sy=y;sthrust=thrust;
        svx=vx;svy=vy;sangle=angle;stimeout=timeout;
        snextCheckPointId=nextCheckPointId;schecked=checked;
        sshieldcount=shieldcount;
    }
    void load(){
        shieldcount=sshieldcount;
        x=sx;y=sy;thrust=sthrust;
        vx=svx;vy=svy;angle=sangle;timeout=stimeout;
        nextCheckPointId=snextCheckPointId;checked=schecked;
    }
    public void block(){
     Pod p=enemyBest();   
     Point t=Player.checkpoints[p.nextCheckPointId];
     if(collision(Player.opods[0]) ||collision(Player.opods[0]))System.out.println((int)(t.x-3*p.vx)+" "+(int)(t.y-3*p.vy)+" SHIELD");
     else{
        System.out.println((int)(t.x-3*p.vx)+" "+(int)(t.y-3*p.vy)+" BOOST"); 
     }

    }
    public Pod enemyBest(){
        Pod tmp=Player.opods[0];
        double d=tmp.distance2(Player.checkpoints[tmp.nextCheckPointId]),dd=0;
        for(Pod p:Player.opods){
            
            dd=p.distance2(Player.checkpoints[p.nextCheckPointId]);
            if(dd<d){
                d=dd;
                tmp=p;
            }
        }
        return tmp;
    }
    public boolean collision(Pod u){
     
        double dist = this.distance2(u);

        // Somme des rs au carré
        double sr = (this.r + u.r)*(this.r + u.r);
    
        // On prend tout au carré pour éviter d'avoir à appeler un sqrt inutilement. C'est mieux pour les performances
    
        if (dist < sr) {
            // Les objets sont déjà l'un sur l'autre. On a donc une collision immédiate
            return true;
        }
    
        // Optimisation. Les objets ont la même vitesse ils ne pourront jamais se rentrer dedans
        if (this.vx == u.vx && this.vy == u.vy) {
            return false;
        }
    
        // On se met dans le référentiel de u. u est donc immobile et se trouve sur le point (0,0) après ça
        double x = this.x - u.x;
        double y = this.y - u.y;
        Point myp = new Point(x, y);
        double vx = this.vx - u.vx;
        double vy = this.vy - u.vy;
        Point up =new Point(0, 0);
        // On cherche le point le plus proche de u (qui est donc en (0,0)) sur la droite décrite par notre vecteur de vitesse
        Point p = up.closest(myp, new Point(x + vx, y + vy));
    
        // Distance au carré entre u et le point le plus proche sur la droite décrite par notre vecteur de vitesse
        double pdist = up.distance2(p);
    
        // Distance au carré entre nous et ce point
        double mypdist = myp.distance2(p);
    
        // Si la distance entre u et cette droite est inférieur à la somme des rs, alors il y a possibilité de collision
        if (pdist < sr) {
            // Notre vitesse sur la droite
            double length = Math.sqrt(vx*vx + vy*vy);
    
            // On déplace le point sur la droite pour trouver le point d'impact
            double backdist = Math.sqrt(sr - pdist);
            p.x = p.x - backdist * (vx / length);
            p.y = p.y - backdist * (vy / length);
    
            // Si le point s'est éloigné de nous par rapport à avant, c'est que notre vitesse ne va pas dans le bon sens
            if (myp.distance2(p) > mypdist) {
                return false;
            }
    
            pdist = p.distance(myp);
    
            // Le point d'impact est plus loin que ce qu'on peut parcourir en un seul tour
            if (pdist > length) {
                return false;
            }
    
            // Temps nécessaire pour atteindre le point d'impact
            double t = pdist / length;
    
            return true;
        }
    
        return false;
    }   
	double facingAngle(Point p){
         double ax=vx-lastVx;  
         double ay=vy-lastVy;  
         return p.getAngle(new Point(ax,ay));
    }
	double diffAngle(Point p) {
	    double a = getAngle(p);

	    // To know whether we should turn clockwise or not we look at the two ways and keep the smallest
	    // The ternary operators replace the use of a modulo operator which would be slower
	    double right = angle <= a ? a - angle : 360 - angle + a;
	    double left = angle >= a ? angle - a : angle + 360 - a;

	    if (right < left) {
	        return right;
	    } else {
	        // We return a negative angle if we must rotate to left
	        return -left;
	    }
	}
	void rotate(Point p) {
	    double a = diffAngle(p);

	    // Can't turn by more than 18° in one turn
	    if (a > 18) {
	        a = 18;
	    } else if (a < -18) {
	        a = -18;
	    }

	    angle += a;

	    // The % operator is slow. If we can avoid it, it's better.
	    if (angle >= 360) {
	        angle = angle - 360;
	    } else if (angle < 0) {
	        angle += 360;
	    }
	}
	void boost(int thrust) {
	  // Don't forget that a pod which has activated its shield cannot accelerate for 3 turns
	    if (shield) {
	        return;
	    }

	    // Conversion of the angle to radiants
	    double ra =(double)( angle * Math.PI / 180);

	    // Trigonometry
	    vx += Math.cos(ra) * thrust;
	    vy += Math.sin(ra) * thrust;
	}
	void move(double t) {
	    x += vx * t;
	    y += vy * t;
	}
	void end() {
	    x = Math.round(x);
	    y = Math.round(y);
	    vx = (int)(vx * 0.85);
	    vy = (int)(vy * 0.85);

	    // Don't forget that the timeout goes down by 1 each turn. It is reset to 100 when you pass a checkpoint
	    timeout -= 1;
	}
	void check(){
	    if(distance(Player.checkpoints[nextCheckPointId])<600){
	     checked++;   
	     timeout=100;
	    }
	}
	void play(Point p, int thrust) {
	    rotate(p);
	    boost(thrust);
	    move(1);
	    check();
	    end();
	}
	void output(Move move) {
	    double a = angle + move.angle;

	    if (a >= 360) {
	        a = a - 360;
	    } else if (a < 0) {
	        a += 360;
	    }

	    // Look for a point corresponding to the angle we want
	    // Multiply by 10000 to limit rounding errors
	    a = (double)(a * Math.PI / 180);
	    double px = (double)(x + Math.cos(a) * 10000);
	    double py = (double)(y + Math.sin(a) * 10000);

	    if (move.shield) {
	        System.out.println(Math.round(px)+" "+Math.round(py)+" SHIELD");
	        //activateShield();
	    } else {
	       // if(move.thrust>100){
	       //     System.out.println(Math.round(px)+" "+ Math.round(py)+" BOOST");return;
	       // }
	        System.out.println(Math.round(px)+" "+ Math.round(py)+" "+move.thrust);
	    }
	}
	double score() {
    	return this.checked*50000 - distance(Player.checkpoints[nextCheckPointId])-timeout;
	}
	void updateShield(){
	 
	 if(shield && shieldcount>0)shieldcount--; 
	 else{
	     shield=false;
	     shieldcount=3;
	 }
	}
	void apply(Move move){
		double a = angle + move.angle;

	    if (a >= 360) {
	        a = a - 360;
	    } else if (a < 0) {
	        a += 360;
	    }

	    // Look for a point corresponding to the angle we want
	    // Multiply by 10000 to limit rounding errors
	    a = (double)(a * Math.PI / 180);
	    double px = (double)(x + Math.cos(a) * 10000);
	    double py = (double)(y + Math.sin(a) * 10000);
        shield=move.shield;
        if(shield) updateShield();
        play(new Point(px,py),move.thrust);
	    
	}
    void play(){
        Point t=Player.checkpoints[nextCheckPointId];
        if(collision(Player.opods[0]) ||collision(Player.opods[0] ))
            System.out.println((int)(t.x-3*vx)+" "+(int)(t.y-3*vy)+" SHIELD"); 
        else
            System.out.println((int)(t.x-3*vx)+" "+(int)(t.y-3*vy)+" BOOST");   
    }
    
}
class Move {
    double angle=0; // Between -18 and +18
    int thrust=100; // Between -1 and 200
    boolean shield=false;
    public Move(){
    }
    public Move(double angle,int thrust,boolean shield){
        this.angle=angle;this.thrust=thrust;this.shield=shield;   
    }
    void mutate(double amplitude) {
	    double ramin = angle - 36* amplitude;
	    double ramax = angle + 36 * amplitude;
	    if (ramin < -18) {
	        ramin = -18;
	    }

	    if (ramax > 18) {
	        ramax = 18;
	    }

        double range = (ramax - ramin) + 1; 
	    angle = (double)((Math.random() * range) + ramin);

	    if (!shield && Math.random()*100 > 80) {
	        shield = true;
	    } else {
	        int pmin = thrust - (int)(101 * amplitude);
	        int pmax = thrust + (int)(101 * amplitude);

	        if (pmin < 0) {
	            pmin = 0;
	        }

	        if (pmax > 101) {
	            pmax = 101;
	        }
            int range2 = (pmax - pmin) + 1; 
	        thrust = (int)(Math.random() * range2) + pmin;

	        shield = false;
	    }
	}

}
class Solution {
    int moves;
    Move[] moves1;
    Move[] moves2;
    public Solution(int moves){
        this.moves=moves;
        moves1=new Move[moves];
        moves2=new Move[moves];
        generateSolution();
    }
    Move generate(){
        double a=0;
        int t=0;
        boolean shield=Math.random()>0.2 && Player.turn>0;
        double d=Math.random();
        int tt0=1;
        if(Player.turn>0)tt0=0;
        if(d<0.35){
            t=100;
        }
        else if(d<0.7){
            t=0;
        }
        else {
            t=(int)Math.random()*100;
        }
        d=Math.random();
        if(d<0.25)a=18+tt0*342;
        else if (d<0.50)a=-18-tt0*342;
        else if (d<0.75)a=0;
        else a=d*(36+tt0*648)-18-tt0*342;
    	Move tmp=new Move(a,t,shield);
    	//tmp.mutate((double)Math.random());
    	return tmp;
    }
    void generateSolution(){
    	for(int i=0;i<moves;i++){
    		moves1[i]=generate();
    		moves2[i]=generate();
    	}
    }
    double score() {
    	for(int i=0;i<2;i++){Player.mypods[i].store();
    	   // System.err.println("Before angle "+Player.mypods[i].angle);
    	}
	    double result = 0;//hum
	    for (int i = 0; i < moves1.length; ++i) {
	        // Apply the moves to the pods before playing
	        Player.mypods[0].apply(moves1[i]);
	        Player.mypods[1].apply(moves2[i]);
	        result+=Player.mypods[0].score()+Player.mypods[1].score();
	    }
	   
	    for(int i=0;i<2;i++){Player.mypods[i].load();
	        //System.err.println("After angle "+Player.mypods[i].angle);
	    }
	    
	    return result;
    }
    void mutate(){
        for(int i=0;i<moves;i++){
    		moves1[i].mutate(Math.random()*0.2);
    		moves2[i].mutate(Math.random()*0.2);
    	}
    }
    
    void crossOver(){
        Move tmp=new Move();
        for(int i=0;i<moves;i++){
            if(i%2==0){
                tmp.angle=moves1[i].angle;
                tmp.thrust=moves1[i].thrust;
                tmp.shield=moves1[i].shield;
                moves1[i].angle=moves2[i].angle;
                moves1[i].thrust=moves2[i].thrust;
                moves1[i].shield=moves2[i].shield;
                moves2[i].angle=tmp.angle;
                moves2[i].thrust=tmp.thrust;
                moves2[i].shield=tmp.shield;
            }else{
                tmp.angle=moves2[i].angle;
                tmp.thrust=moves2[i].thrust;
                tmp.shield=moves2[i].shield;
                moves2[i].angle=moves1[i].angle;
                moves2[i].thrust=moves1[i].thrust;
                moves2[i].shield=moves1[i].shield;
                moves1[i].angle=tmp.angle;
                moves1[i].thrust=tmp.thrust;
                moves1[i].shield=tmp.shield;
            }
    		moves1[i].mutate(Math.random()*0.05);
    		moves2[i].mutate(Math.random()*0.05);
    	}
    }
    public String toString(){
     
        String s="";
        for(int i=0;i<moves;i++){
            s+="[Move1 "+moves1[i].angle+" "+moves1[i].thrust+" ]";
            s+="[Move2 "+moves2[i].angle+" "+moves2[i].thrust+" ]";
        }
        s+=score();
        return s;
    }
}

class Player {

    public static Pod[] mypods;
    public static Pod[] opods;
    public static CheckPoint[] checkpoints;
    static int deep=8;
    static Solution[] solutionsPool=new Solution[8];
    static int pools=0;
    static int turn=0;
    static Pod blocker,racer;
    public static void main(String args[]) {
        
        mypods=new Pod[2];
        opods=new Pod[2];
        Scanner in = new Scanner(System.in);
        int laps = in.nextInt();
        int checkpointCount = in.nextInt();
        
        
        if(turn==0){
            checkpoints=new CheckPoint[checkpointCount];
            
            for (int i = 0; i < checkpointCount; i++) {
                int checkpointX = in.nextInt();
                int checkpointY = in.nextInt();
                
                checkpoints[i]=new CheckPoint(checkpointX,checkpointY,i);
            }
            
            deep=checkpointCount;
        }
        // game loop
        while (true) {
            
            for (int i = 0; i < 2; i++) {
                int x = in.nextInt(); // x position of your pod
                int y = in.nextInt(); // y position of your pod
                int vx = in.nextInt(); // x speed of your pod
                int vy = in.nextInt(); // y speed of your pod
                int angle = in.nextInt(); // angle of your pod
                int nextCheckPointId = in.nextInt(); // next check point id of your pod
                if(turn==0)mypods[i]=new Pod(x,y,vx,vy,angle,nextCheckPointId);
                else mypods[i].update(x,y,vx,vy,angle,nextCheckPointId);
                // mypods[i].play(); 
                System.err.println("After angle "+angle);
            }
            
            for (int i = 0; i < 2; i++) {
                int x = in.nextInt(); // x position of the opponent's pod
                int y = in.nextInt(); // y position of the opponent's pod
                int vx = in.nextInt(); // x speed of the opponent's pod
                int vy = in.nextInt(); // y speed of the opponent's pod
                int angle = in.nextInt(); // angle of the opponent's pod
                int nextCheckPointId = in.nextInt(); // next check point id of the opponent's pod
                if(turn==0) opods[i]=new Pod(x,y,vx,vy,angle,nextCheckPointId);
                else  opods[i].update(x,y,vx,vy,angle,nextCheckPointId);
            }       
            
            int gens=0;
            int tt =1;
            if(turn==0)tt=1;
            else tt=0;
            double score=-1000000000;
            Solution tmp=null,s=null;
            long millis = System.currentTimeMillis();
            System.err.println("Facing angle"+mypods[0].facingAngle(checkpoints[mypods[0].nextCheckPointId])+ " angle"+mypods[0].angle);
            
            while(System.currentTimeMillis()-millis<140+800*tt){
                s=new Solution(1);
                gens++;
               // s.mutate();
               // s.crossOver();
                // if(solutionsPool[pools]==null)s=new Solution(5);
                // else s=solutionsPool[pools];s.mutate();
                double a=s.score();
                if(a>score){
                 score=a;tmp=s;   
                }
            }
            // if(pools<7){
            //     solutionsPool[pools]=tmp;pools++;
            // }else {
            //  pools=0;  
            // }
            // if(mypods[0].check==0){
            //     for(int i=0;i<2;i++)mypods[i].play();
            // }else{
            if(turn>0)mypods[0].block();//output(tmp.moves1[0]);
            else mypods[0].play();
             mypods[1].play();//output(tmp.moves2[0]);   
            //}
            for(int i=0;i<2;i++)mypods[i].check();
            
            turn++;
            System.err.println("Message"+gens);
            
            
        }
    }
}