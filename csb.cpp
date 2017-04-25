
#define SHIELD_PROB 20
#define X 5
#define moves 6
const int SHIELD = - 1;
float amplitude=1.0;
float minScore=-1;
class Point
{
	
public:
	float x,y,sx,sy;
	Point();
	~Point();
	float distance2(Point p){
		return (p.x-x)*(p.x-x)+(p.y-y)*(p.y-y);
	}
	float distance(Point p){
		return sqrt(distance2(p));
	}
	Point closest(Point a, Point b) {
	    float da = b.y - a.y;
	    float db = a.x - b.x;
	    float c1 = da*a.x + db*a.y;
	    float c2 = -db*this.x + da*this.y;
	    float det = da*da + db*db;
	    float cx = 0;
	    float cy = 0;

	    if (det != 0) {
	        cx = (da*c1 - db*c2) / det;
	        cy = (da*c2 + db*c1) / det;
	    } else {
	        // The point is already on the line
	        cx = this.x;
	        cy = this.y;
	    }

	    return new Point(cx, cy);
	}
	virtual void save(){
		sx = x;
        sy = y;
	}
	virtual void reset(){
		x = sx;
        y = sy;
	}
	
};
class Unit : public Point
{
public:
	int id;
	float r,vx,vy;
	Unit();
	~Unit();
	Collision collision(Unit u) {
	    // Square of the distance
	    float dist = this.distance2(u);

	    // Sum of the radii squared
	    float sr = (this.r + u.r)*(this.r + u.r);

	    // We take everything squared to avoid calling sqrt uselessly. It is better for performances

	    if (dist < sr) {
	        // Objects are already touching each other. We have an immediate collision.
	        return new Collision(this, u, 0.0);
	    }

	    // Optimisation. Objects with the same speed will never collide
	    if (this.vx == u.vx && this.vy == u.vy) {
	        return null;
	    }

	    // We place ourselves in the reference frame of u. u is therefore stationary and is at (0,0)
	    float x = this.x - u.x;
	    float y = this.y - u.y;
	    Point myp = new Point(x, y);
	    float vx = this.vx - u.vx;
	    float vy = this.vy - u.vy;
	    Point up = new Point(0, 0)

	    // We look for the closest point to u (which is in (0,0)) on the line described by our speed vector
	    Point p = up.closest(myp, new Point(x + vx, y + vy));

	    // Square of the distance between u and the closest point to u on the line described by our speed vector
	    float pdist = up.distance2(p);

	    // Square of the distance between us and that point
	    float mypdist = myp.distance2(p);

	    // If the distance between u and this line is less than the sum of the radii, there might be a collision
	    if (pdist < sr) {
	     // Our speed on the line
	        float length = sqrt(vx*vx + vy*vy);

	        // We move along the line to find the point of impact
	        float backdist = sqrt(sr - pdist);
	        p.x = p.x - backdist * (vx / length);
	        p.y = p.y - backdist * (vy / length);

	        // If the point is now further away it means we are not going the right way, therefore the collision won't happen
	        if (myp.distance2(p) > mypdist) {
	            return null;
	        }

	        pdist = p.distance(myp);

	        // The point of impact is further than what we can travel in one turn
	        if (pdist > length) {
	            return null;
	        }

	        // Time needed to reach the impact point
	        float t = pdist / length;

	        return new Collision(this, u, t);
	    }

	    return null;
	}
	void bounce(Unit u) {
	    if (u instanceof Checkpoint) {
	        // Collision with a checkpoint
	       this.timeout=100;
			this.checked+=1;
	    } else {
	        // If a pod has its shield active its mass is 10 otherwise it's 1
	        float m1 = this.shield ? 10 : 1;
	        float m2 = u.shield ? 10 : 1;
	        float mcoeff = (m1 + m2) / (m1 * m2);

	        float nx = this.x - u.x;
	        float ny = this.y - u.y;

	        // Square of the distance between the 2 pods. This value could be hardcoded because it is always 800²
	        float nxnysquare = nx*nx + ny*ny;

	        float dvx = this.vx - u.vx;
	        float dvy = this.vy - u.vy;

	        // fx and fy are the components of the impact vector. product is just there for optimisation purposes
	        float product = nx*dvx + ny*dvy;
	        float fx = (nx * product) / (nxnysquare * mcoeff);
	        float fy = (ny * product) / (nxnysquare * mcoeff);

	        // We apply the impact vector once
	        this.vx -= fx / m1;
	        this.vy -= fy / m1;
	        u.vx += fx / m2;
	        u.vy += fy / m2;

	        // If the norm of the impact vector is less than 120, we normalize it to 120
	        float impulse = sqrt(fx*fx + fy*fy);
	        if (impulse < 120.0) {
	            fx = fx * 120.0 / impulse;
	            fy = fy * 120.0 / impulse;
	        }

	        // We apply the impact vector a second time
	        this.vx -= fx / m1;
	        this.vy -= fy / m1;
	        u.vx += fx / m2;
	        u.vy += fy / m2;

	        // This is one of the rare places where a Vector class would have made the code more readable.
	        // But this place is called so often that I can't pay a performance price to make it more readable.
	    }
	}
	
	virtual void print() {}

    virtual void save() {
    	Point::save();
        svx = vx;
        svy = vy;
    }

    virtual void reset() {
        Point::reset();
        vx = svx;
        vy = svy;
    }
	
};
class Pod : public Unit
{
public:
	float angle,sangle;
	int nextCheckpointId,snextCheckpointId,checked,schecked,timeout,stimeout;
	Pod partener;
	bool shield,sshield;

	Pod();
	~Pod();
	float getAngle(Point p) {
	    float d = this.distance(p);
	    float dx = (p.x - this.x) / d;
	    float dy = (p.y - this.y) / d;

	    // Simple trigonometry. We multiply by 180.0 / PI to convert radiants to degrees.
	    float a = acos(dx) * 180.0 / PI;

	    // If the point I want is below me, I have to shift the angle for it to be correct
	    if (dy < 0) {
	        a = 360.0 - a;
	    }

	    return a;
	}
	float diffAngle(Point p) {
	    float a = this.getAngle(p);

	    // To know whether we should turn clockwise or not we look at the two ways and keep the smallest
	    // The ternary operators replace the use of a modulo operator which would be slower
	    float right = this.angle <= a ? a - this.angle : 360.0 - this.angle + a;
	    float left = this.angle >= a ? this.angle - a : this.angle + 360.0 - a;

	    if (right < left) {
	        return right;
	    } else {
	        // We return a negative angle if we must rotate to left
	        return -left;
	    }
	}
	void rotate(Point p) {
	    float a = this.diffAngle(p);

	    // Can't turn by more than 18° in one turn
	    if (a > 18.0) {
	        a = 18.0;
	    } else if (a < -18.0) {
	        a = -18.0;
	    }

	    this.angle += a;

	    // The % operator is slow. If we can avoid it, it's better.
	    if (this.angle >= 360.0) {
	        this.angle = this.angle - 360.0;
	    } else if (this.angle < 0.0) {
	        this.angle += 360.0;
	    }
	}
	void boost(int thrust) {
	  // Don't forget that a pod which has activated its shield cannot accelerate for 3 turns
	    if (this.shield) {
	        return;
	    }

	    // Conversion of the angle to radiants
	    float ra = this.angle * PI / 180.0;

	    // Trigonometry
	    this.vx += cos(ra) * thrust;
	    this.vy += sin(ra) * thrust;
	}
	void move(float t) {
	    this.x += this.vx * t;
	    this.y += this.vy * t;
	}
	void end() {
	    this.x = round(this.x);
	    this.y = round(this.y);
	    this.vx = truncate(this.vx * 0.85);
	    this.vy = truncate(this.vy * 0.85);

	    // Don't forget that the timeout goes down by 1 each turn. It is reset to 100 when you pass a checkpoint
	    this.timeout -= 1;
	}
	void play(Point p, int thrust) {
	    this.rotate(p);
	    this.boost(thrust);
	    this.move(1.0);
	    this.end();
	}
	
	void output(Move move) {
	    float a = this.angle + move.angle;

	    if (a >= 360.0) {
	        a = a - 360.0;
	    } else if (a < 0.0) {
	        a += 360.0;
	    }

	    // Look for a point corresponding to the angle we want
	    // Multiply by 10000.0 to limit rounding errors
	    a = a * PI / 180.0;
	    float px = this.x + cos(a) * 10000.0;
	    float py = this.y + sin(a) * 10000.0;

	    if (move.shield) {
	        print(round(px), round(py), "SHIELD");
	        activateShield();
	    } else {
	        print(round(px), round(py), move.power);
	    }
	}
	float score() {
    	return this.checked*50000 - this.distance(checkpoints[this.nextCheckpointId]);
	}
	void apply(Move move){
		this.angle=move.angle;
		this.shield=move.shield;
		this.thrust=move.thrust;
	}


	 virtual void save() {
        Unit::save();
        sangle=angle;
		snextCheckpointId=nextCheckpointId;
		schecked,checked;
		stimeout,timeout;
		spartener=partener;
		sshield=shield;
    }

    virtual void reset() {
        Unit::reset();
        angle=sangle;
		nextCheckpointId=snextCheckpointId;
		checked=schecked;
		timeout=stimeout;
		partener=spartener;
		shield=sshield;
    }
};
class Collision {
	public:
	float t;
   	Unit a,b;
	Collision();
	~Collision();
  
};
class Checkpoint : public Unit
{
public:
	Checkpoint();
	~Checkpoint();

};
class Move {
    float angle=0; // Between -18.0 and +18.0
    int thrust=100; // Between -1 and 200
    bool shield=false;

    void mutate(float amplitude) {
	    float ramin = this.angle - 36.0 * amplitude;
	    float ramax = this.angle + 36.0 * amplitude;

	    if (ramin < -18.0) {
	        ramin = -18.0;
	    }

	    if (ramax > 18.0) {
	        ramax = 18.0;
	    }

	    angle = random(ramin, ramax);

	    if (!this.shield && random(0, 100) < SHIELD_PROB) {
	        this.shield = true;
	    } else {
	        int pmin = this.thrust - 200 * amplitude;
	        int pmax = this.thrust + 200 * amplitude;

	        if (pmin < 0) {
	            pmin = 0;
	        }

	        if (pmax > 0) {
	            pmax = 200;
	        }

	        this.thrust = random(pmin, pmax);

	        this.thrust = false;
	    }
	}

};
class Solution {
    Move moves1[moves];
    Move moves2[moves];
    Move generate(){
    	Move tmp;
    	tmp.angle=random(-18,18);
    	tmp.thrust=random(-1,100);
    	tmp.shield=tmp.thrust==-1;
    	return tmp;

    }
    Solution generateSolution(){
    	for(int i(0);i<moves;i++){
    		moves1[i]=generate();
    		moves2[i]=generate();
    	}
    	return this;
    }
    float score() {

    	// Reset everyone to their initial states
	    store();//hum
	    // Play out the turns
	    // Compute the score
	    float result = 0//hum
	    for (int i = 0; i < moves1.length; ++i) {
	        // Apply the moves to the pods before playing
	        myPod1.apply(moves1[i]);//hum
	        myPod2.apply(moves2[i]);//hum

	        play(pods,checkpoints);//hum
	        result+=myPod1.score()+myPod2.score();
	    }
	    // Reset everyone to their initial states
	    load();//hum

	    return result;
}
   
};
Solution[] generatePopulation(){
	Solution tmp[X];
	Solution s;
	for(int i(0);i<X;i++){
		tmp[i]=s.generateSolution();
	}
	return tmp;
}
void play(Pod[] pods, Checkpoint[] checkpoints) {
    // This tracks the time during the turn. The goal is to reach 1.0
    float t = 0.0;

    while (t < 1.0) {
        Collision firstCollision = null;

        // We look for all the collisions that are going to occur during the turn
        for (int i = 0; i < pods.length; ++i) {
            // Collision with another pod?
            for (int j = i + 1; j < pods.length; ++j) {
                Collision col = pods[i].collision(pods[j]);

                // If the collision occurs earlier than the one we currently have we keep it
                if (col != null && col.t + t < 1.0 && (firstCollision == null || col.t < firstCollision.t)) {
                    firstCollision = col;
                }
            }

            // Collision with another checkpoint?
            // It is unnecessary to check all checkpoints here. We only test the pod's next checkpoint.
            // We could look for the collisions of the pod with all the checkpoints, but if such a collision happens it wouldn't impact the game in any way
            Collision col = pods[i].collision(checkpoints[pods[i].nextCheckpointId]);

            // If the collision happens earlier than the current one we keep it
            if (col != null && col.t + t < 1.0 && (firstCollision == null || col.t < firstCollision.t)) {
                firstCollision = col;
            }
        }

        if (firstCollision == null) {
            // No collision, we can move the pods until the end of the turn
            for (int i = 0; i < pods.length; ++i) {
                pods[i].move(1.0 - t);
            }

            // End of the turn
            t = 1.0;
        } else {
            // Move the pods to reach the time `t` of the collision
            for (int i = 0; i < pods.length; ++i) {
                pods[i].move(firstCollision.t);
            }

            // Play out the collision
            firstCollision.a.bounce(firstCollision.b);

            t += firstCollision.t;
        }
    }

    for (int i = 0; i < pods.length; ++i) {
        pods[i].end();
    }
}


void test(){
	time=time();
	Solution[] solutions = generatePopulation();
	while (time < 150) {
	    Solution solution = solutions[random(0, X)].mutate();

	    if (solution.score() > minScore) {
	        keepSolution();
	    }
	    time=time()-time;
	}
}
