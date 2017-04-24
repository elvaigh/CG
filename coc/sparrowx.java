import java.io.IOException;
import java.io.InputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class Player {


 static final int MAP_WIDTH = 23;
 static final int MAP_HEIGHT = 21;
 static final int COOLDOWN_CANNON = 2;
 static final int COOLDOWN_MINE = 5;
 static final int INITIAL_SHIP_HEALTH = 100;
 static final int MAX_SHIP_HEALTH = 100;
 static final int MAX_SHIP_SPEED=2;
 static final int MIN_SHIPS = 1;
 static final int MAX_SHIPS=3;
 static final int MIN_MINES=5;
 static final int MAX_MINES=25;
 static final int MIN_RUM_BARRELS = 10;
 static final int MAX_RUM_BARRELS = 26;
 static final int MIN_RUM_BARREL_VALUE = 10;
 static final int MAX_RUM_BARREL_VALUE = 20;
 static final int REWARD_RUM_BARREL_VALUE = 30;
 static final int MINE_VISIBILITY_RANGE = 5;
 static final int FIRE_DISTANCE_MAX = 10;
 static final int LOW_DAMAGE = 25;
 static final int HIGH_DAMAGE = 50;
 static final int MINE_DAMAGE = 25;
 static final int NEAR_MINE_DAMAGE = 10;
 static final boolean CANNONS_ENABLED=true;
 static final boolean MINES_ENABLED=true;

public static void main(String args[]) {
    Bot bot = new Bot();
    Game game = new Game();
    Timer timer = new Timer();
    Scanner in = new Scanner(System.in);
    while (true) {
        timer.begin();
        game.update(in);
        bot.play(game);
        timer.end();
        System.err.println("Message "+timer.elapsedTime);
    }
}
}

class Timer {
    
    long startTime;
    long stopTime;
    long elapsedTime;
    
    public void begin() {
        startTime = System.currentTimeMillis();
    }

    public void end() {
        stopTime = System.currentTimeMillis();
        elapsedTime = stopTime - startTime;
    }
}

class Bot  {
        int id;
        List<Ship> ships;
        List<Ship> shipsAlive;

        public Bot() {
            this.ships = new ArrayList<>();
            this.shipsAlive = new ArrayList<>();
        }

        public void setDead() {
            for (Ship ship : ships) {
                ship.health = 0;
            }
        }

        public int getScore() {
            int score = 0;
            for (Ship ship : ships) {
                score += ship.health;
            }
            return score;
        }

        public List<String> toViewString() {
            List<String> data = new ArrayList<>();

            data.add(String.valueOf(this.id));
            for (Ship ship : ships) {
                data.add(ship.toViewString());
            }

            return data;
        }
        public void play(Game game) {
            this.shipsAlive=game.myShips;
            for(int i=0;i<game.myShipCount;i++)
            System.out.println("WAIT");
        }

}

class Game {
    int turn = 0;
    int myShipCount;
    int entityCount;

    List<Ship> myShips=new ArrayList<Ship>();
    List<Ship> hisShips=new ArrayList<Ship>();
    List<RumBarrel> barrels=new ArrayList<RumBarrel>();
    List<Mine> mines=new ArrayList<Mine>();
    List<Cannonball> cannonballs=new ArrayList<Cannonball>();
     List<Coord> cannonBallExplosions=new ArrayList<Coord>();

    public void update(Scanner in) {
        updateCount(in);
        updateEntities(in);
        turn++;
    }

    void updateCount(Scanner in) {
        myShipCount = in.nextInt();
        entityCount = in.nextInt();
    }

     void updateEntities(Scanner in) {
        for (int i = 0; i < entityCount; i++) {
            getEntity(in);
        }
    }

    public void getEntity(Scanner in) {
        int id = in.nextInt();
        String type = in.next();
        int x = in.nextInt();
        int y = in.nextInt();
        int arg1,arg2,arg3,arg4;
        arg1 = in.nextInt();
        arg2 = in.nextInt();
        arg3 = in.nextInt();
        arg4 = in.nextInt();
        
        if(type.equals("SHIP")){
           Ship  ship=new Ship(x,y,arg1,arg2,arg3,arg4);
            if (arg4==0)
                hisShips.add(ship);
            else
                myShips.add(ship);
            
       }
        else if(type.equals("BARREL"))
            barrels.add(new  RumBarrel(x, y, arg1));
        else if(type.equals("MINE"))
            mines.add(new Mine(x,y));
        else 
             cannonballs.add(new Cannonball(x,y,arg1,arg3,arg4,arg2));
        
    }

     void decrementRum() {
        for (Ship ship : myShips) {
            ship.damage(1);
        }
        for (Ship ship : hisShips) {
            ship.damage(1);
        }
    }

     void updateInitialRum() {
        for (Ship ship : myShips) {
            ship.initialHealth = ship.health;
        }
        for (Ship ship : hisShips) {
            ship.initialHealth = ship.health;
        }
    }
     void moveCannonballs() {
        for (Iterator<Cannonball> it = cannonballs.iterator(); it.hasNext();) {
            Cannonball ball = it.next();
            if (ball.remainingTurns == 0) {
                it.remove();
                continue;
            } else if (ball.remainingTurns > 0) {
                ball.remainingTurns--;
            }

            if (ball.remainingTurns == 0) {
                cannonBallExplosions.add(ball.position);
            }
        }
    }
     void checkBarrelCollisions(Ship ship) {
        Coord bow = ship.bow();
        Coord stern = ship.stern();
        Coord center = ship.position;

        for (Iterator<RumBarrel> it = barrels.iterator(); it.hasNext();) {
            RumBarrel barrel = it.next();
            if (barrel.position.equals(bow) || barrel.position.equals(stern) || barrel.position.equals(center)) {
                ship.heal(barrel.health);
                it.remove();
            }
        }
    }

     void checkCollisions() {
        // Check collisions with Barrels
        for (Ship ship : this.myShips) {
            checkBarrelCollisions(ship);
        }
        for (Ship ship : this.hisShips) {
            checkBarrelCollisions(ship);
        }

        // Check collisions with Mines
       checkMineCollisions();
    }

  void checkMineCollisions() {
        for (Iterator<Mine> it = mines.iterator(); it.hasNext();) {
            Mine mine = it.next();
             mine.explode(myShips, false);
             mine.explode(hisShips, false);

           
        }
    }
      void moveShips(Bot player ) {
        // ---
        // Go forward
        // ---
        for (int i = 1; i <= Player.MAX_SHIP_SPEED; i++) {
                for (Ship ship : player.shipsAlive) {
                    ship.newPosition = ship.position;
                    ship.newBowCoordinate = ship.bow();
                    ship.newSternCoordinate = ship.stern();

                    if (i > ship.speed) {
                        continue;
                    }

                    Coord newCoordinate = ship.position.neighbor(ship.orientation);

                    if (newCoordinate.isInsideMap()) {
                        // Set new coordinate.
                        ship.newPosition = newCoordinate;
                        ship.newBowCoordinate = newCoordinate.neighbor(ship.orientation);
                        ship.newSternCoordinate = newCoordinate.neighbor((ship.orientation + 3) % 6);
                    } else {
                        // Stop ship!
                        ship.speed = 0;
                    }
                }

            // Check ship and obstacles collisions
            List<Ship> collisions = new ArrayList<>();
            boolean collisionDetected = true;
            while (collisionDetected) {
                collisionDetected = false;

                for (Ship ship : this.myShips) {
                    if (ship.newBowIntersect(myShips)) {
                        collisions.add(ship);
                    }
                }
                for (Ship ship : this.hisShips) {
                    if (ship.newBowIntersect(hisShips)) {
                        collisions.add(ship);
                    }
                }

                for (Ship ship : collisions) {
                    // Revert last move
                    ship.newPosition = ship.position;
                    ship.newBowCoordinate = ship.bow();
                    ship.newSternCoordinate = ship.stern();

                    // Stop ships
                    ship.speed = 0;

                    collisionDetected = true;
                }
                collisions.clear();
            }

            // Move ships to their new location
            for (Ship ship : this.myShips) {
                ship.position = ship.newPosition;
            }
            for (Ship ship : this.hisShips) {
                ship.position = ship.newPosition;
            }

            checkCollisions();
        }
    }

     void rotateShips(Bot player) {
        // Rotate
        for (Ship ship : player.shipsAlive) {
            ship.newPosition = ship.position;
            ship.newBowCoordinate = ship.newBow();
            ship.newSternCoordinate = ship.newStern();
        }

        // Check collisions
        boolean collisionDetected = true;
        List<Ship> collisions = new ArrayList<>();
        while (collisionDetected) {
            collisionDetected = false;

            for (Ship ship : this.myShips) {
                if (ship.newPositionsIntersect(this.myShips)) {
                    collisions.add(ship);
                }
            }
            for (Ship ship : this.hisShips) {
                if (ship.newPositionsIntersect(this.hisShips)) {
                    collisions.add(ship);
                }
            }

            for (Ship ship : collisions) {
                ship.newOrientation = ship.orientation;
                ship.newBowCoordinate = ship.newBow();
                ship.newSternCoordinate = ship.newStern();
                ship.speed = 0;
                collisionDetected = true;
            }

            collisions.clear();
        }

        // Apply rotation
        for (Ship ship : this.myShips) {
            ship.orientation = ship.newOrientation;
        }
         for (Ship ship : this.hisShips) {
            ship.orientation = ship.newOrientation;
        }

        checkCollisions();
    }

    

    void explodeShips() {
        for (Iterator<Coord> it = cannonBallExplosions.iterator(); it.hasNext();) {
            Coord position = it.next();
            for (Ship ship : myShips) {
                if (position.equals(ship.bow()) || position.equals(ship.stern())) {
                    ship.damage(Player.LOW_DAMAGE);
                    it.remove();
                    break;
                } else if (position.equals(ship.position)) {
                    ship.damage(Player.HIGH_DAMAGE);
                    it.remove();
                    break;
                }
            }
            for (Ship ship : hisShips) {
                if (position.equals(ship.bow()) || position.equals(ship.stern())) {
                    ship.damage(Player.LOW_DAMAGE);
                    it.remove();
                    break;
                } else if (position.equals(ship.position)) {
                    ship.damage(Player.HIGH_DAMAGE);
                    it.remove();
                    break;
                }
            }
        }
    }

    void explodeMines() {
        for (Iterator<Coord> itBall = cannonBallExplosions.iterator(); itBall.hasNext();) {
            Coord position = itBall.next();
            for (Iterator<Mine> it = mines.iterator(); it.hasNext();) {
                Mine mine = it.next();
                if (mine.position.equals(position)) {
                    mine.explode(myShips, true);
                    mine.explode(hisShips, true);
                    it.remove();
                    itBall.remove();
                    break;
                }
            }
        }
    }

    void explodeBarrels() {
        for (Iterator<Coord> itBall = cannonBallExplosions.iterator(); itBall.hasNext();) {
            Coord position = itBall.next();
            for (Iterator<RumBarrel> it = barrels.iterator(); it.hasNext();) {
                RumBarrel barrel = it.next();
                if (barrel.position.equals(position)) {
                    it.remove();
                    itBall.remove();
                    break;
                }
            }
        }
    }


    protected void updateGame(int round,Bot player) {
        moveCannonballs();
        decrementRum();
        updateInitialRum();

        applyActions(player);
        moveShips(player);
        rotateShips(player);

        explodeShips();
        explodeMines();
        explodeBarrels();

        // For each sunk ship, create a new rum barrel with the amount of rum the ship had at the begin of the turn (up to 30).
        for (Ship ship : myShips) {
            if (ship.health <= 0) {
                int reward = Math.min(Player.REWARD_RUM_BARREL_VALUE, ship.initialHealth);
                if (reward > 0) {
                    barrels.add(new RumBarrel(ship.position.x, ship.position.y, reward));
                }
            }
        }
        for (Ship ship : hisShips) {
            if (ship.health <= 0) {
                int reward = Math.min(Player.REWARD_RUM_BARREL_VALUE, ship.initialHealth);
                if (reward > 0) {
                    barrels.add(new RumBarrel(ship.position.x, ship.position.y, reward));
                }
            }
        }

        

        for (Iterator<Ship> it = myShips.iterator(); it.hasNext();) {
            Ship ship = it.next();
            if (ship.health <= 0) {
                player.shipsAlive.remove(ship);
                it.remove();
            }
        }
        for (Iterator<Ship> it = hisShips.iterator(); it.hasNext();) {
            Ship ship = it.next();
            if (ship.health <= 0) {
                it.remove();
            }
        }
    }
     void applyActions(Bot player) {
            for (Ship ship : player.shipsAlive) {
                if (ship.mineCooldown > 0) {
                    ship.mineCooldown--;
                }
                if (ship.cannonCooldown > 0) {
                    ship.cannonCooldown--;
                }

                ship.newOrientation = ship.orientation;

                if (ship.action != null) {
                    switch (ship.action) {
                    case FASTER:
                        if (ship.speed < Player.MAX_SHIP_SPEED) {
                            ship.speed++;
                        }
                        break;
                    case SLOWER:
                        if (ship.speed > 0) {
                            ship.speed--;
                        }
                        break;
                    case PORT:
                        ship.newOrientation = (ship.orientation + 1) % 6;
                        break;
                    case STARBOARD:
                        ship.newOrientation = (ship.orientation + 5) % 6;
                        break;
                    case MINE:
                        if (ship.mineCooldown == 0) {
                            Coord target = ship.stern().neighbor((ship.orientation + 3) % 6);

                            if (target.isInsideMap()) {
                                boolean cellIsFreeOfBarrels = barrels.stream().noneMatch(barrel -> barrel.position.equals(target));
                                boolean cellIsFreeOfMines = mines.stream().noneMatch(mine -> mine.position.equals(target));
                                boolean cellIsFreeOfMyShips = myShips.stream().filter(b -> b != ship).noneMatch(b -> b.at(target));
                                boolean cellIsFreeOfHisShips = hisShips.stream().filter(b -> b != ship).noneMatch(b -> b.at(target));

                                if (cellIsFreeOfBarrels &&cellIsFreeOfMines  && cellIsFreeOfMyShips &&cellIsFreeOfHisShips ) {
                                    ship.mineCooldown = Player.COOLDOWN_MINE;
                                    Mine mine = new Mine(target.x, target.y);
                                    mines.add(mine);
                                }
                            }

                        }
                        break;
                    case FIRE:
                        int distance = ship.bow().distanceTo(ship.target);
                        if (ship.target.isInsideMap() && distance <= Player.FIRE_DISTANCE_MAX && ship.cannonCooldown == 0) {
                            int travelTime = (int) (1 + Math.round(ship.bow().distanceTo(ship.target) / 3.0));
                            cannonballs.add(new Cannonball(ship.target.x, ship.target.y, ship.id, ship.bow().x, ship.bow().y, travelTime));
                            ship.cannonCooldown = Player.COOLDOWN_CANNON;
                        }
                        break;
                    default:
                        break;
                    }
                }
        }
    }

}


enum Action {
    FASTER, SLOWER, PORT, STARBOARD, FIRE, MINE,WAIT
}

enum EntityType {
    SHIP, BARREL, MINE, CANNONBALL
}

class Coord {
     final static int[][] DIRECTIONS_EVEN = new int[][] { { 1, 0 }, { 0, -1 }, { -1, -1 }, { -1, 0 }, { -1, 1 }, { 0, 1 } };
     final static int[][] DIRECTIONS_ODD = new int[][] { { 1, 0 }, { 1, -1 }, { 0, -1 }, { -1, 0 }, { 0, 1 }, { 1, 1 } };
    final int x;
    final int y;

    public Coord(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Coord(Coord other) {
        this.x = other.x;
        this.y = other.y;
    }

    public double angle(Coord targetPosition) {
        double dy = (targetPosition.y - this.y) * Math.sqrt(3) / 2;
        double dx = targetPosition.x - this.x + ((this.y - targetPosition.y) & 1) * 0.5;
        double angle = -Math.atan2(dy, dx) * 3 / Math.PI;
        if (angle < 0) {
            angle += 6;
        } else if (angle >= 6) {
            angle -= 6;
        }
        return angle;
    }

    CubeCoordinate toCubeCoordinate() {
        int xp = x - (y - (y & 1)) / 2;
        int zp = y;
        int yp = -(xp + zp);
        return new CubeCoordinate(xp, yp, zp);
    }

    Coord neighbor(int orientation) {
        int newY, newX;
        if (this.y % 2 == 1) {
            newY = this.y + DIRECTIONS_ODD[orientation][1];
            newX = this.x + DIRECTIONS_ODD[orientation][0];
        } else {
            newY = this.y + DIRECTIONS_EVEN[orientation][1];
            newX = this.x + DIRECTIONS_EVEN[orientation][0];
        }

        return new Coord(newX, newY);
    }

    boolean isInsideMap() {
        return x >= 0 && x < Player.MAP_WIDTH && y >= 0 && y < Player.MAP_HEIGHT;
    }

    int distanceTo(Coord dst) {
        return this.toCubeCoordinate().distanceTo(dst.toCubeCoordinate());
    }

    
    public boolean equals(Object obj) {
        if (obj == null || getClass() != obj.getClass()) {
            return false;
        }
        Coord other = (Coord) obj;
        return y == other.y && x == other.x;
    }

    
    public String toString() {
        return " ttot";
        //return join(x, y);
    }
}

class CubeCoordinate {
    static int[][] directions = new int[][] { { 1, -1, 0 }, { +1, 0, -1 }, { 0, +1, -1 }, { -1, +1, 0 }, { -1, 0, +1 }, { 0, -1, +1 } };
    int x, y, z;

    public CubeCoordinate(int x, int y, int z) {
        this.x = x;
        this.y = y;
        this.z = z;
    }

    Coord toOffsetCoordinate() {
        int newX = x + (z - (z & 1)) / 2;
        int newY = z;
        return new Coord(newX, newY);
    }

    CubeCoordinate neighbor(int orientation) {
        int nx = this.x + directions[orientation][0];
        int ny = this.y + directions[orientation][1];
        int nz = this.z + directions[orientation][2];

        return new CubeCoordinate(nx, ny, nz);
    }

    int distanceTo(CubeCoordinate dst) {
        return (Math.abs(x - dst.x) + Math.abs(y - dst.y) + Math.abs(z - dst.z)) / 2;
    }

    
    public String toString() {
        return " ttot";//return join(x, y, z);
    }
}



 class Entity {
   
    protected  int id;
    protected  EntityType type;
    protected Coord position;
    
    public Entity(){
        super();
        
    }
    public Entity(EntityType type, int x, int y) {
        this.type = type;
        this.position = new Coord(x, y);
    }

    public String toViewString() {
        return " ttot";
        //return join(id, position.y, position.x);
    }

    protected String toPlayerString(int arg1, int arg2, int arg3, int arg4) {
        return " ttot";
        //return join(id, type.name(), position.x, position.y, arg1, arg2, arg3, arg4);
    }
}

class Mine extends Entity {
    public Mine(int x, int y) {
        super(EntityType.MINE, x, y);
    }

    public String toPlayerString(int playerIdx) {
        return toPlayerString(0, 0, 0, 0);
    }

    public void explode(List<Ship> ships, boolean force) {
        
        Ship victim = null;

        for (Ship ship : ships) {
            if (position.equals(ship.bow()) || position.equals(ship.stern()) || position.equals(ship.position)) {
                ship.damage(Player.MINE_DAMAGE);
                victim = ship;
            }
        }

        if (force || victim != null) {
            

            for (Ship ship : ships) {
                if (ship != victim) {
                    Coord impactPosition = null;
                    if (ship.stern().distanceTo(position) <= 1) {
                        impactPosition = ship.stern();
                    }
                    if (ship.bow().distanceTo(position) <= 1) {
                        impactPosition = ship.bow();
                    }
                    if (ship.position.distanceTo(position) <= 1) {
                        impactPosition = ship.position;
                    }

                    if (impactPosition != null) {
                        ship.damage(Player.NEAR_MINE_DAMAGE);
                    }
                }
            }
        }

    }
}

class Cannonball extends Entity {
    final int ownerEntityId;
    final int srcX;
    final int srcY;
    final int initialRemainingTurns;
    int remainingTurns;

    public Cannonball(int row, int col, int ownerEntityId, int srcX, int srcY, int remainingTurns) {
        super(EntityType.CANNONBALL, row, col);
        this.ownerEntityId = ownerEntityId;
        this.srcX = srcX;
        this.srcY = srcY;
        this.initialRemainingTurns = this.remainingTurns = remainingTurns;
    }

    public String toViewString() {
        return " ttot";//return join(id, position.y, position.x, srcY, srcX, initialRemainingTurns, remainingTurns, ownerEntityId);
    }

    public String toPlayerString(int playerIdx) {
        return toPlayerString(ownerEntityId, remainingTurns, 0, 0);
    }
}

class RumBarrel extends Entity {
     int health;

    public RumBarrel(int x, int y, int health) {
        super(EntityType.BARREL, x, y);
        this.health = health;
    }

    public String toViewString() {
       return " ttot";// return join(id, position.y, position.x, health);
    }

    public String toPlayerString(int playerIdx) {
        return toPlayerString(health, 0, 0, 0);
    }
}


class Damage {
     final Coord position;
     final int health;
     final boolean hit;

    public Damage(Coord position, int health, boolean hit) {
        this.position = position;
        this.health = health;
        this.hit = hit;
    }

    public String toViewString() {
        return " ttot";//return join(position.y, position.x, health, (hit ? 1 : 0));
    }
}

class Ship extends Entity {
    int orientation;
    int speed;
    int health;
    int initialHealth;
    int owner;
    String message;
    Action action;
    int mineCooldown;
    int cannonCooldown;
    Coord target;
    public int newOrientation;
    public Coord newPosition;
    public Coord newBowCoordinate;
    public Coord newSternCoordinate;

    public Ship(int x, int y, int _orientation,int _speed,int _health ,int _owner) {
        super(EntityType.SHIP, x, y);
        this.orientation = _orientation;
        this.initialHealth=100;
        this.speed = _speed;
        this.health =_health;
        this.owner = _owner;
        action=Action.WAIT;
    }

    public String toViewString() {
        return " ttot";
        // return join(id, position.y, position.x, orientation, health, speed, (action != null ? action : "WAIT"), bow().y, bow().x, stern().y,
        //         stern().x, " ;" + (message != null ? message : ""));
    }

    public String toPlayerString(int playerIdx) {
        return toPlayerString(orientation, speed, health, owner == playerIdx ? 1 : 0);
    }

    public void setMessage(String message) {
        if (message != null && message.length() > 50) {
            message = message.substring(0, 50) + "...";
        }
        this.message = message;
    }

    public void moveTo(int x, int y) {
        Coord currentPosition = this.position;
        Coord targetPosition = new Coord(x, y);

        if (currentPosition.equals(targetPosition)) {
            this.action = Action.SLOWER;
            return;
        }

        double targetAngle, angleStraight, anglePort, angleStarboard, centerAngle, anglePortCenter, angleStarboardCenter;

        switch (speed) {
        case 2:
            this.action = Action.SLOWER;
            break;
        case 1:
            // Suppose we've moved first
            currentPosition = currentPosition.neighbor(orientation);
            if (!currentPosition.isInsideMap()) {
                this.action = Action.SLOWER;
                break;
            }

            // Target reached at next turn
            if (currentPosition.equals(targetPosition)) {
                this.action = null;
                break;
            }

            // For each neighbor cell, find the closest to target
            targetAngle = currentPosition.angle(targetPosition);
            angleStraight = Math.min(Math.abs(orientation - targetAngle), 6 - Math.abs(orientation - targetAngle));
            anglePort = Math.min(Math.abs((orientation + 1) - targetAngle), Math.abs((orientation - 5) - targetAngle));
            angleStarboard = Math.min(Math.abs((orientation + 5) - targetAngle), Math.abs((orientation - 1) - targetAngle));

            centerAngle = currentPosition.angle(new Coord(Player.MAP_WIDTH / 2, Player.MAP_HEIGHT / 2));
            anglePortCenter = Math.min(Math.abs((orientation + 1) - centerAngle), Math.abs((orientation - 5) - centerAngle));
            angleStarboardCenter = Math.min(Math.abs((orientation + 5) - centerAngle), Math.abs((orientation - 1) - centerAngle));

            // Next to target with bad angle, slow down then rotate (avoid to turn around the target!)
            if (currentPosition.distanceTo(targetPosition) == 1 && angleStraight > 1.5) {
                this.action = Action.SLOWER;
                break;
            }

            Integer distanceMin = null;

            // Test forward
            Coord nextPosition = currentPosition.neighbor(orientation);
            if (nextPosition.isInsideMap()) {
                distanceMin = nextPosition.distanceTo(targetPosition);
                this.action = null;
            }

            // Test port
            nextPosition = currentPosition.neighbor((orientation + 1) % 6);
            if (nextPosition.isInsideMap()) {
                int distance = nextPosition.distanceTo(targetPosition);
                if (distanceMin == null || distance < distanceMin || distance == distanceMin && anglePort < angleStraight - 0.5) {
                    distanceMin = distance;
                    this.action = Action.PORT;
                }
            }

            // Test starboard
            nextPosition = currentPosition.neighbor((orientation + 5) % 6);
            if (nextPosition.isInsideMap()) {
                int distance = nextPosition.distanceTo(targetPosition);
                if (distanceMin == null || distance < distanceMin
                        || (distance == distanceMin && angleStarboard < anglePort - 0.5 && this.action == Action.PORT)
                        || (distance == distanceMin && angleStarboard < angleStraight - 0.5 && this.action == null)
                        || (distance == distanceMin && this.action == Action.PORT && angleStarboard == anglePort
                                && angleStarboardCenter < anglePortCenter)
                        || (distance == distanceMin && this.action == Action.PORT && angleStarboard == anglePort
                                && angleStarboardCenter == anglePortCenter && (orientation == 1 || orientation == 4))) {
                    distanceMin = distance;
                    this.action = Action.STARBOARD;
                }
            }
            break;
        case 0:
            // Rotate ship towards target
            targetAngle = currentPosition.angle(targetPosition);
            angleStraight = Math.min(Math.abs(orientation - targetAngle), 6 - Math.abs(orientation - targetAngle));
            anglePort = Math.min(Math.abs((orientation + 1) - targetAngle), Math.abs((orientation - 5) - targetAngle));
            angleStarboard = Math.min(Math.abs((orientation + 5) - targetAngle), Math.abs((orientation - 1) - targetAngle));

            centerAngle = currentPosition.angle(new Coord(Player.MAP_WIDTH / 2, Player.MAP_HEIGHT / 2));
            anglePortCenter = Math.min(Math.abs((orientation + 1) - centerAngle), Math.abs((orientation - 5) - centerAngle));
            angleStarboardCenter = Math.min(Math.abs((orientation + 5) - centerAngle), Math.abs((orientation - 1) - centerAngle));

            Coord forwardPosition = currentPosition.neighbor(orientation);

            this.action = null;

            if (anglePort <= angleStarboard) {
                this.action = Action.PORT;
            }

            if (angleStarboard < anglePort || angleStarboard == anglePort && angleStarboardCenter < anglePortCenter
                    || angleStarboard == anglePort && angleStarboardCenter == anglePortCenter && (orientation == 1 || orientation == 4)) {
                this.action = Action.STARBOARD;
            }

            if (forwardPosition.isInsideMap() && angleStraight <= anglePort && angleStraight <= angleStarboard) {
                this.action = Action.FASTER;
            }
            break;
        }

    }

    public void faster() {
        this.action = Action.FASTER;
    }

    public void slower() {
        this.action = Action.SLOWER;
    }

    public void port() {
        this.action = Action.PORT;
    }

    public void starboard() {
        this.action = Action.STARBOARD;
    }

    public void placeMine() {
      
            this.action = Action.MINE;
        
    }

    public Coord stern() {
        return position.neighbor((orientation + 3) % 6);
    }

    public Coord bow() {
        return position.neighbor(orientation);
    }

    public Coord newStern() {
        return position.neighbor((newOrientation + 3) % 6);
    }

    public Coord newBow() {
        return position.neighbor(newOrientation);
    }

    public boolean at(Coord coord) {
        Coord stern = stern();
        Coord bow = bow();
        return stern != null && stern.equals(coord) || bow != null && bow.equals(coord) || position.equals(coord);
    }

    public boolean newBowIntersect(Ship other) {
        return newBowCoordinate != null && (newBowCoordinate.equals(other.newBowCoordinate) || newBowCoordinate.equals(other.newPosition)
                || newBowCoordinate.equals(other.newSternCoordinate));
    }

    public boolean newBowIntersect(List<Ship> ships) {
        for (Ship other : ships) {
            if (this != other && newBowIntersect(other)) {
                return true;
            }
        }
        return false;
    }

    public boolean newPositionsIntersect(Ship other) {
        boolean sternCollision = newSternCoordinate != null && (newSternCoordinate.equals(other.newBowCoordinate)
                || newSternCoordinate.equals(other.newPosition) || newSternCoordinate.equals(other.newSternCoordinate));
        boolean centerCollision = newPosition != null && (newPosition.equals(other.newBowCoordinate) || newPosition.equals(other.newPosition)
                || newPosition.equals(other.newSternCoordinate));
        return newBowIntersect(other) || sternCollision || centerCollision;
    }

    public boolean newPositionsIntersect(List<Ship> ships) {
        for (Ship other : ships) {
            if (this != other && newPositionsIntersect(other)) {
                return true;
            }
        }
        return false;
    }

    public void damage(int health) {
        this.health -= health;
        if (this.health <= 0) {
            this.health = 0;
        }
    }

    public void heal(int health) {
        this.health += health;
        if (this.health > 100) {
            this.health = 100;
        }
    }

    public void fire(int x, int y) {
      
            Coord target = new Coord(x, y);
            this.target = target;
            this.action = Action.FIRE;
        
    }
}
