import java.util.*;
import java.io.*;
import java.math.*;

class Point{

     double x,y,sx,sy;
     public Point(double x,double y){
      this.x=x;
      this.y=y;
     }
     public double dist2(double x,double y){
      double dx=(x-this.x);
      double dy=(y-this.y);
      return dx*dx+dy*dy;
    }
     public double dist2(Point p){
          double  dx=(p.x-this.x);
          double dy=(p.y-this.y);
          return dx*dx+dy*dy;
     }
     public double dist(Point p){return Math.sqrt(dist2(p));}
     public double dist(double x,double y){return Math.sqrt(dist2(x,y));}
     double getAngle(Point p) {
        double d = dist(p);
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
}
class Unit extends Point{
    private Double[] cache=new Double[5];
    int id, type;
    double r, vx, vy;
    public Unit(double x,double y){super(x,y);}
    void bounce(Unit u) {};
    double collision_time(Unit u) {
        if (vx == u.vx && vy == u.vy) {
            return -1;
        }

        double sr2 ;
        if(u.type == Player.CP)sr2=357604;
        else sr2=640000;

        double dx = x - u.x;
        double dy = y - u.y;
        double dvx = vx - u.vx;
        double dvy = vy - u.vy;
        double a = dvx*dvx + dvy*dvy;

        if (a < Player.E) return -1;

        double b = -2.0*(dx*dvx + dy*dvy);
        double delta = b*b - 4.0*a*(dx*dx + dy*dy - sr2);

        if (delta < 0.0) return -1;

        double t = (b - Math.sqrt(delta))*(1.0/(2.0*a));

        if (t <= 0.0 || t > 1.0) return -1;

        return t;
    }
    void save() {
        cache[0] = x;
        cache[1] = y;
        cache[2] = vx;
        cache[3] = vy;
    }

    void load() {
        x = cache[0];
        y = cache[1];
        vx = cache[2];
        vy = cache[3];
    }
}
class CheckPoint extends Unit{

    public CheckPoint(int id, double x, double y) {
        super(x,y);
        this.id = id;
        this.vx = this.vy = 0;
        this.type = Player.CP;
        this.r = 600;
    }

    void bounce(Unit u){}
}

class Collision {
    Unit a;
    Unit b;
    double t;

    public Collision() {}

    public Collision(Unit a, Unit b, double t) {
        this.a = a;
        this.b = b;
        this.t = t;
    }
}
class Pod extends Unit{

    double angle = -1;
    double next_angle = -1;
    boolean has_boost,shas_boost;
    int ncpid, checked, timeout, shield;
    Pod partner;
    // TODO maybe replace cache array with primitives?
    private Double[] cache=new Double[10];
    public Pod(int id) {
        super(0,0);
        this.id = id;
        this.r = 400;
        this.type = Player.POD;
        this.ncpid = 1;
        // TODO move timeout to global/team var
        this.timeout = 100;
        this.has_boost = true;
        this.checked =0;
        this.shield = 0;
    }
    double score(){
        return checked*50000 - this.dist(Player.cps[this.ncpid]);
    }
    void apply(int thrust, double angle) {
        angle = Math.max((double)-18., Math.min((double)18., angle));
        this.angle += angle;
        if (this.angle >= 360.) {
            this.angle = this.angle - 360.;
        } else if (this.angle < 0.0) {
            this.angle += 360.;
        }

        if (thrust == -1) {
            this.shield = 4;
        } else {
            boost(thrust);
        }
    }
    void rotate(Point p) {
        double a = diff_angle(p);
        a = Math.max((double)-18., Math.min((double)18., a));

        angle += a;
        if (angle >= 360.) {
            angle = angle - 360.;
        } else if (angle < 0.0) {
            angle += 360.;
        }
    }
    void boost(int thrust) {
        if (shield > 0) return;

        double ra = angle * Math.PI / 180.0;

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

        if (checked >= Player.cp_ct * Player.laps) {
            ncpid = 0;
            checked = Player.cp_ct * Player.laps;
        }
        timeout--;
        if (shield > 0) shield--;
    }
    void bounce(Unit u) {
        if (u.type == Player.CP) {
            checked += 1;
            timeout = partner.timeout = 100;
            ncpid = (ncpid + 1) % Player.cp_ct;
            return;
        }

        bounce_w_pod((Pod)u);
    }
    void bounce_w_pod(Pod u) {
        double m1 = shield == 4 ? 10 : 1;
        double m2 = u.shield == 4 ? 10 : 1;
        double mcoeff = (m1 + m2) / (m1 * m2);

        double nx = x - u.x;
        double ny = y - u.y;
        double dst2 = nx*nx + ny*ny;
        double dvx = vx - u.vx;
        double dvy = vy - u.vy;
        double prod = (nx*dvx + ny*dvy) / (dst2 * mcoeff);
        double fx = nx * prod;
        double fy = ny * prod;
        double m1_inv = 1.0 / m1;
        double m2_inv = 1.0 / m2;

        vx -= fx * m1_inv;
        vy -= fy * m1_inv;
        u.vx += fx * m2_inv;
        u.vy += fy * m2_inv;

        double impulse = Math.sqrt(fx*fx + fy*fy);
        if (impulse < 120) {
            double df = 120.0 / impulse;
            fx *= df;
            fy *= df;
        }

        vx -= fx * m1_inv;
        vy -= fy * m1_inv;
        u.vx += fx * m2_inv;
        u.vy += fy * m2_inv;
    }
    double diff_angle(Point p) {
        double a = get_angle(p);
        double right = angle <= a ? a - angle : 360 - angle + a;
        double left = angle >= a ? angle - a : angle + 360 - a;

        if (right < left) {
            return right;
        }
        return -left;
    }
    double get_angle(Point p) {
        double d = this.dist(p);
        double dx = (p.x - x) / d;
        double dy = (p.y - y) / d;

        double a = Math.acos(dx) * 180 / Math.PI;

        if (dy < 0) {
            a = 360 - a;
        }

        return a;
    }
    void update(int x, int y, int vx, int vy, double angle, int ncpid) {
        if (shield > 0) shield--;
        if (ncpid != this.ncpid) {
            timeout = partner.timeout = 100;
            checked++;
        } else {
            timeout--;
        }

        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.ncpid = ncpid;

        if (Player.is_p2 && id > 1) swap(angle, this.next_angle);
        this.angle = angle;
        if (Player.r == 0) this.angle = 1 + diff_angle(Player.cps[1]);
        save();
    }
    void swap(double a,double b){
        double tmp=a;
        a=b;
        b=tmp;
    }
    void update(int shield, boolean has_boost) {
        this.shield = shield;
        this.has_boost = has_boost;
    }
    void save() {
        super.save();
        cache[0] =(double) ncpid;
        cache[1] = (double)checked;
        cache[2] = (double)timeout;
        cache[3] = (double)shield;
        cache[4] = angle;
        shas_boost=has_boost;
    }
    void load() {
        super.load();
        ncpid   = cache[0].intValue();
        checked = cache[1].intValue();
        timeout = cache[2].intValue();
        shield  = cache[3].intValue();
        angle   = cache[4];
        has_boost = shas_boost;
    }
}

class Solution {

    double score = -1;
    Integer[] thrusts=new Integer[Player.DEPTH*2];
    Double[] angles=new Double[Player.DEPTH*2];

    public Solution(boolean with_rnd) {
        if (with_rnd) randomize();
    }

    void shift() {
        for (int i = 1; i < Player.DEPTH; i++) {
            angles[i-1]        = angles[i];
            thrusts[i-1]       = thrusts[i];
            angles[i-1+Player.DEPTH]  = angles[i+Player.DEPTH];
            thrusts[i-1+Player.DEPTH] = thrusts[i+Player.DEPTH];
        }
        randomize(Player.DEPTH-1, true);
        randomize(2*Player.DEPTH-1, true);
        score = -1;
    }

    void mutate() {
        randomize(Player.rnd(2*Player.DEPTH),false);
    }

    void mutate(Solution child) {
        child.angles=angles.clone();
        child.thrusts=thrusts.clone();
       
        child.mutate();
        child.score = -1;
    }

    void randomize(int idx, boolean full) {
        int r = Player.rnd(2);
        if (full || r == 0) angles[idx] = Math.max(-18, Math.min(18, (double)Player.rnd(-40, 40)));

        if (full || r == 1) {
            if (Player.rnd(100) >= Player.SHIELD_PROB) {
                thrusts[idx] =(int) Math.max(0, Math.min(Player.MAX_THRUST, Player.rnd((int) -0.5*Player.MAX_THRUST, 2*Player.MAX_THRUST)));
            } else {
                thrusts[idx] = -1;
            }
        }
        score = -1;
    }

    void randomize() {
        for (int i = 0; i < 2*Player.DEPTH; i++) randomize(i, true);
    }
}

class Bot {
    int id = 0;

    public Bot() {};

    public Bot(int id) {
        this.id = id;
    }

    void move(){}

    Pod runner() {
        return runner(Player.pods[id], Player.pods[id+1]);
    }

    Pod blocker() {
        return blocker(Player.pods[id], Player.pods[id+1]);
    }

    Pod runner(Pod pod0, Pod pod1) {
        return pod0.score() - pod1.score() >= -1000 ? pod0 : pod1;
    }

    Pod blocker(Pod pod0, Pod pod1) {
        return runner(pod0, pod1).partner;
    }
}

class ReflexBot extends Bot{

    public ReflexBot() {}

    public ReflexBot(int id) {
        this.id = id;
    }

    void move() {
        move_runner(false);
        move_blocker(false);
    }

    void move_as_main() {
        move_runner(true);
        move_blocker(true);
    }

    void move_runner(boolean for_output) {
        Pod pod = !for_output ? runner() : Player.pods[0];

        CheckPoint cp = Player.cps[pod.ncpid];
        Point t=new Point(cp.x - 3*pod.vx, cp.y - 3*pod.vy);
        double raw_angle = pod.diff_angle(t);

        int thrust = Math.abs(raw_angle) < 90 ? Player.MAX_THRUST : 0;
        double angle = Math.max((double) -18, Math.min((double) 18, raw_angle));

        if (!for_output) pod.apply(thrust, angle);
        else Player.print_move(thrust, angle, pod);
    }

    void move_blocker(boolean for_output) {
        Pod pod = !for_output ? blocker() : Player.pods[1];

        CheckPoint cp = Player.cps[pod.ncpid];
        Point t=new Point(cp.x - 3*pod.vx, cp.y - 3*pod.vy);
        double raw_angle = pod.diff_angle(t);

        int thrust = Math.abs(raw_angle) < 90 ? Player.MAX_THRUST : 0;
        double angle =Math.max((double) -18, Math.min((double) 18, raw_angle));

        if (!for_output) pod.apply(thrust, angle);
        else Player.print_move(thrust, angle, pod);
    }
}

class SearchBot extends Bot{

    Solution sol=new Solution(true);
    Bot[] oppBots=new Bot[2];

    public SearchBot() {}

    public SearchBot(int id) {
        this.id = id;
    }

    void move(Solution sol) {
        Player.pods[id].apply(sol.thrusts[Player.turn], sol.angles[Player.turn]);
        Player.pods[id+1].apply(sol.thrusts[Player.turn+Player.DEPTH], sol.angles[Player.turn+Player.DEPTH]);
    }

    void move() {
        move(sol);
    }

    void solve(double time, boolean with_seed) {
        Solution best=new Solution(true);
        if (with_seed) {
            best = sol;
            best.shift();
        } else {
            best.randomize();
            if (Player.r == 0 && Player.pods[id].dist(Player.cps[1]) > 4000) best.thrusts[0] = 650;
        }
        get_score(best);
        double tmp=System.currentTimeMillis();
        Solution child=new Solution(true);
        while (System.currentTimeMillis()-tmp < time) {
            best.mutate(child);
            if (get_score(child) > get_score(best)) best = child;
        }
        sol = best;
    }

    double get_score(Solution sol) {
        if (sol.score == -1) {
            double score=100000000;
            for (Bot oppBot : oppBots) {
                score=Math.min(score,get_bot_score(sol, oppBot));
            }
            sol.score = score;
        }

        return sol.score;
    }

    double get_bot_score(Solution sol, Bot opp) {
        double score = 0;
        while (Player.turn < Player.DEPTH) {
            move(sol);
            opp.move();
            Player.play();
            if (Player.turn == 0) score += 0.1*evaluate();
            Player.turn++;
        }
        score += 0.9*evaluate();
        Player.load();

        if (Player.r > 0) Player.sols_ct++;

        return score;
    }

    double evaluate() {
        Pod my_runner = runner(Player.pods[id], Player.pods[id+1]);
        Pod my_blocker = blocker(Player.pods[id], Player.pods[id+1]);
        Pod opp_runner = runner(Player.pods[(id+2) % 4], Player.pods[(id+3) % 4]);
        Pod opp_blocker = blocker(Player.pods[(id+2) % 4], Player.pods[(id+3) % 4]);

        if (my_runner.timeout <= 0) return -1e7;
        if (opp_runner.timeout <= 0) return 1e7;
        if (opp_runner.checked == Player.laps*Player.cp_ct || opp_blocker.checked == Player.laps*Player.cp_ct) return -1e7;
        if (my_runner.checked == Player.laps*Player.cp_ct || my_blocker.checked == Player.laps*Player.cp_ct) return 1e7;

        double score = my_runner.score() - opp_runner.score();
        score -= my_blocker.dist(Player.cps[opp_runner.ncpid]);
        score -= Math.abs(my_blocker.diff_angle(opp_runner));

        return score;
    }
}

class Player {

    static int CP  = 0;
    static int POD = 1;
    static int DEPTH = 6;
    static double SHIELD_PROB = 10;
    static int MAX_THRUST = 100;
    static double E = 0.00001;
    static int r = -1;
    static int turn = 0;
    static int sols_ct = 0;
    static boolean is_p2 = false;
    static int cp_ct, laps;
    static Pod[] pods=new Pod[4];
    static CheckPoint[] cps=new CheckPoint[10];
    static void load() {
        for (int i = 0; i < 4; i++) pods[i].load();
        turn = 0;
    }
    static void play() {
        double t = 0.0;
        while (t < 1.0) {
            Collision first_col = new Collision(null, null, -1);
            for (int i = 0; i < 4; i++) {
                for (int j = i + 1; j < 4; j++) {
                    double col_time = pods[i].collision_time(pods[j]);
                    if (col_time > -1 && col_time + t < 1.0 && (first_col.t == -1 || col_time < first_col.t)) {
                        first_col.a = pods[i];
                        first_col.b = pods[j];
                        first_col.t = col_time;
                    }
                }

                // TODO this is wasteful, get rid of it
                double col_time = pods[i].collision_time(cps[pods[i].ncpid]);
                if (col_time > -1 && col_time + t < 1.0 && (first_col.t == -1 || col_time < first_col.t)) {
                    first_col.a = pods[i];
                    first_col.b = cps[pods[i].ncpid];
                    first_col.t = col_time;
                }
            }

            if (first_col.t == -1) {
                for (int i = 0; i < 4; i++) {
                    pods[i].move(1.0 - t);
                }
                t = 1.0;
            } else {
                for (int i = 0; i < 4; i++) {
                    pods[i].move(first_col.t);
                }

                first_col.a.bounce(first_col.b);
                t += first_col.t;
            }
        }

        for (int i = 0; i < 4; i++) {
            pods[i].end();
        }
    }
    static void print_move(int thrust, double angle, Pod pod) {
        double a = pod.angle + angle;

        if (a >= 360.0) {
            a = a - 360.0;
        } else if (a < 0.0) {
            a += 360.0;
        }

        a = a * Math.PI / 180.0;
        double px = pod.x + Math.cos(a) * 10000.0;
        double py = pod.y + Math.sin(a) * 10000.0;

        if (thrust == -1) {
           System.out.println((int) Math.round(px)+" "+ (int) Math.round(py)+" SHIELD");
            pod.shield = 4;
        } else if (thrust == 650) {
            pod.has_boost = false;
            System.out.println((int) Math.round(px)+" "+ (int) Math.round(py)+" BOOST");
        } else {
            System.out.println((int) Math.round(px)+" "+ (int) Math.round(py)+" "+thrust);
        }
    }
    static int fastrand() {
        int g_seed = 42;
        g_seed = (214013*g_seed+2531011);
        return (g_seed>>16)&0x7FFF;
    }
    static int rnd(int b) {
        return fastrand() % b;
    }
    static int rnd(int a, int b) {
        return a + rnd(b - a + 1);
    }
    public static void main(String args[]) {
        
       
        Scanner in = new Scanner(System.in);
        laps = in.nextInt();
        cp_ct= in.nextInt();
        for (int i = 0; i < cp_ct; i++) {
            int cx, cy;
            cx=in.nextInt();
            cy=in.nextInt();
            cps[i] = new CheckPoint(i, cx, cy);
        }

        for (int i = 0; i < 4; i++) pods[i] = new Pod(i);

        Player.pods[0].partner = Player.pods[1];
        Player.pods[1].partner = Player.pods[0];
        Player.pods[2].partner = Player.pods[3];
        Player.pods[3].partner = Player.pods[2];

        ReflexBot me_reflex=new ReflexBot(0);
        ReflexBot opp_reflex=new ReflexBot(2);

        SearchBot opp=new SearchBot(2);
        opp.oppBots[1]=me_reflex;

        SearchBot me=new SearchBot(0);
        me.oppBots[1]=opp;
        me.oppBots[0]=opp_reflex;
        opp.oppBots[0]=me;
        // game loop
        while (true) {
             r++;

            for (int i = 0; i < 4; i++) {
                int x, y, vx, vy, angle, ncpid;
                x= in.nextInt();
                y= in.nextInt();
                vx= in.nextInt();
                vy= in.nextInt();
                angle= in.nextInt();
                ncpid= in.nextInt();
                if (r == 0 && i > 1 && angle > -1) is_p2 = true;
                Player.pods[i].update(x, y, vx, vy, angle, ncpid);
            }

            double time_limit = r>0 ? 0.142 : 0.98;
          
            opp.solve(time_limit*0.15,false);
            me.solve(time_limit, r > 0);
            if (r > 0)System.err.println("Avg iters: " +sols_ct / r + "; Avg sims: " +sols_ct*DEPTH / r) ;
            print_move(me.sol.thrusts[0], me.sol.angles[0], Player.pods[0]);
            print_move(me.sol.thrusts[DEPTH], me.sol.angles[DEPTH], Player.pods[1]);
            
           
        }
    }
}