import java.util.*;
import java.io.*;
import java.math.*;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
 class LostException extends Exception
{
      //
      public LostException() {}

      // Constructor that accepts a message
      public LostException(String message)
      {
         super(message);
      }
      
 }
class Player {

    public static int GAME_VERSION = 2;

    public static final int GOT_PUSHED = 2;
    public static final int DID_PUSH = 1;
    public static final int NO_PUSH = 0;
    public static final int FINAL_HEIGHT = 4;
    public static final int VIEW_DISTANCE = 1;
    public static final int GENERATED_MAP_SIZE = 6;
    public static boolean WIN_ON_MAX_HEIGHT = true;
    public static boolean FOG_OF_WAR = false;
    public static boolean CAN_PUSH = false;
    public static int UNITS_PER_Bot = 1;

    static enum Direction {
        NW, N, NE, W, E, SW, S, SE
    }
    static class Point {
        final int x, y;

        public Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        
        public String toString() {
            return "Point [x=" + x + ", y=" + y + "]";
        }

        
        public int hashCode() {
            final int prime = 31;
            int result = 1;
            result = prime * result + x;
            result = prime * result + y;
            return result;
        }

        
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null) return false;
            if (getClass() != obj.getClass()) return false;
            Point other = (Point) obj;
            return x == other.x && y == other.y;
        }

        int distance(Point other) {
            return Math.max(Math.abs(x - other.x), Math.abs(y - other.y));
        }
    }

    static class Unit {
        int index;
        Bot Bot;
        Point position;
        boolean gotPushed;
        ActionResult did;

        public Unit(Bot Bot, int index) {
            this.Bot = Bot;
            this.index = index;
        }

        public void reset() {
            gotPushed = false;
            did = null;
        }
         public void setPosition(Point _position) {
            this.position=_position;
        }

        public boolean pushed() {
            return did != null && did.type == Action.PUSH;
        }

        public boolean moved() {
            return did != null && did.type == Action.MOVE;
        }

    }

    static class ActionResult {

        public Point moveTarget;
        public Point placeTarget;
        public boolean placeValid;
        public boolean moveValid;
        public boolean scorePoint;
        public String type;
        public Unit unit;

        public ActionResult(String type) {
            this.type = type;
        }

    }

    static class Action {
        public static String MOVE = "MOVE&BUILD";
        public static String PUSH = "PUSH&BUILD";

        int index;
        Direction move;
        Direction place;
        String command;

        public Action(String command, int index, Direction move, Direction place) {
            this.index = index;
            this.move = move;
            this.place = place;
            this.command = command;
        }

        public String toBotString() {
            return command + " " + index + " " + move + " " + place;
        }
    }

    static class Grid {
        private Map<Point, Integer> map;
        int size;

        public Grid() {
            this.map = new HashMap<>();
        }

        public Integer get(int x, int y) {
            return get(new Point(x, y));
        }

        public Integer get(Point p) {
            Integer level = map.get(p);
            return level;
        }

        public void create(Point point) {
            map.put(point, 0);
        }
        public void create(int x, int y) {
            map.put(new Point(x, y), 0);
        }
        public void update(int x, int y,int h) {
            map.put(new Point(x, y), h);
        }

        public void place(Point placeAt) {
            map.put(placeAt, map.get(placeAt) + 1);
        }
    }

    static class Bot {
        int index, score;
        boolean dead, won;
        List<Unit> units;
        private String message;

        public Bot(int index) {
            this.index = index;
            units = new ArrayList<>();
            score = 0;
        }

        public void win() {
            won = true;
        }

        public void die(int round) {
            dead = true;
        }

        public void reset() {
            message = null;
            units.stream().forEach(Unit::reset);
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
            if (message != null && message.length() > 48) {
                this.message = message.substring(0, 46) + "...";
            }

        }
    }
    
    protected boolean isTurnBasedGame() {
        return true;
    }

    
    protected boolean gameIsOver() {
        if (WIN_ON_MAX_HEIGHT) {
            return  Bots.stream().anyMatch(p -> p.won || p.dead);
        }

        boolean oneDead = Bots.get(0).dead;
        boolean twoDead = Bots.get(1).dead;
        if (oneDead && twoDead) {
            return true;
        } else if (oneDead && !twoDead) {
            return Bots.get(1).score > Bots.get(0).score;
        } else if (!oneDead && twoDead) {
            return Bots.get(0).score > Bots.get(1).score;
        } else {
            return false;
        }
    }

    
    static void initGame(int BotCount,int size) {
        if (GAME_VERSION >= 1) {
            WIN_ON_MAX_HEIGHT = false;
        }
        if (GAME_VERSION >= 2) {
            UNITS_PER_Bot = 2;
            CAN_PUSH = true;
        }

        if (GAME_VERSION >= 3) {
            FOG_OF_WAR = true;
        }
        grid = initGrid(size);
        Bots = new ArrayList<Bot>(BotCount);
        units = new ArrayList<Unit>(BotCount * UNITS_PER_Bot);
        for (int idx = 0; idx < BotCount; ++idx) {
            Bot Bot = new Bot(idx);
            for (int i = 0; i < UNITS_PER_Bot; ++i) {
                Unit u = new Unit(Bot, i);
                Bot.units.add(u);
                units.add(u);
            }
            Bots.add(Bot);
        }

    }

    private static Grid initGrid(int size) {
        Grid grid = new Grid();
        grid.size=size;
        for(int i=0;i<size;i++){
            for(int j=0;j<size;j++){
                grid.create(j,i);
            }
        }
        return grid;
    }
    public static void update(int y,String row){
        int h=-1;
        for(int i=0;i<grid.size;i++){
            char c=row.charAt(i);
            if(c!='.'){
                h=Character.getNumericValue(c);
            }
            grid.update(i,y,h);
        }
    }
    private int countIslands(Grid grid, int size) {
        Set<Point> computed = new HashSet<>();

        int total = 0;
        for (Point p : grid.map.keySet()) {
            if (!computed.contains(p)) {
                total++;
                Queue<Point> fifo = new LinkedList<>();
                fifo.add(p);
                while (!fifo.isEmpty()) {
                    Point e = fifo.poll();
                    for (Direction d : Direction.values()) {
                        Point n = getNeighbor(d.name(), e, size);
                        if (!computed.contains(n) && grid.get(n) != null) {
                            fifo.add(n);
                        }
                    }
                    computed.add(e);
                }
            }
        }
        return total;
    }
    
    protected String[] getInputForBot(int round, int BotIdx) {
        List<String> lines = new ArrayList<>();
        Bot self = Bots.get(BotIdx);
        Bot other = Bots.get((BotIdx + 1) % 2);

        for (int y = 0; y < grid.size; ++y) {
            StringBuilder row = new StringBuilder();
            for (int x = 0; x < grid.size; ++x) {
                Integer height = grid.get(x, y);
                if (height == null) {
                    row.append(".");
                } else {
                    row.append(height);
                }
            }
            lines.add(row.toString());
        }
        
        List<Action> legalActions = getLegalActions(self);
        lines.add(String.valueOf(legalActions.size()));
        for (Action action : legalActions) {
            lines.add(action.toBotString());
        }
        return lines.toArray(new String[lines.size()]);
    }

    private boolean unitVisibleToBot(Unit unit, Bot Bot) {
        if (!FOG_OF_WAR)
            return true;
        for (Unit u : Bot.units) {
            if (u.position.distance(unit.position) <= VIEW_DISTANCE) {
                return true;
            }
        }
        return false;
    }

    private ActionResult computeMove(Unit unit, String dir1, String dir2) {

        Point target = getNeighbor(dir1, unit.position);
        Integer targetHeight = grid.get(target);
       
        int currentHeight = grid.get(unit.position);
    
        Point placeTarget = getNeighbor(dir2, target);
        Integer placeTargetHeight = grid.get(placeTarget);
                

        ActionResult result = new ActionResult(Action.MOVE);
        result.moveTarget = target;
        result.placeTarget = placeTarget;

        Optional<Unit> possibleUnit = getUnitOnPoint(placeTarget).filter(u -> !u.equals(unit));
        if (!possibleUnit.isPresent()) {
            result.placeValid = true;
            result.moveValid = true;
        } else if (FOG_OF_WAR && !unitVisibleToBot(possibleUnit.get(), unit.Bot)) {
            result.placeValid = false;
            result.moveValid = true;
        }

        if (targetHeight == FINAL_HEIGHT - 1) {
            result.scorePoint = true;
        }
        result.unit = unit;
        return result;
    }

    private Optional<Unit> getUnitOnPoint(Point target) {
        Optional<Unit> potentialUnit = units.stream().filter(u -> u.position.equals(target)).findFirst();
        return potentialUnit;
    }
    private boolean validPushDirection(String target, String push) {
        if (target.length() == 2) {
            return push.equals(target) || push.equals(target.substring(0, 1)) || push.equals(target.substring(1, 2));
        } else {
            return push.contains(target);
        }
    }
    private ActionResult computePush(Unit unit, String dir1, String dir2) throws LostException {
        if (!validPushDirection(dir1, dir2)) {
            throw new LostException("PushInvalid");
        }
        Point target = getNeighbor(dir1, unit.position);
        Optional<Unit> maybePushed = getUnitOnPoint(target);
        if (!maybePushed.isPresent()) {
            throw new LostException("PushVoid");
        }
        Unit pushed = maybePushed.get();
        
        if (pushed.Bot == unit.Bot) {
            throw new LostException("FriendlyFire");
        }
        
        Point pushTo = getNeighbor(dir2, pushed.position);
        Integer toHeight = grid.get(pushTo);
        int fromHeight = grid.get(target);

        if (toHeight == null || toHeight >= FINAL_HEIGHT || toHeight > fromHeight + 1) {
            throw new LostException("PushInvalid");
        }

        ActionResult result = new ActionResult(Action.PUSH);
        result.moveTarget = pushTo;
        result.placeTarget = target;

        Optional<Unit> possibleUnit = getUnitOnPoint(pushTo);
        if (!possibleUnit.isPresent()) {
            result.placeValid = true;
            result.moveValid = true;
        } else if (FOG_OF_WAR && !unitVisibleToBot(possibleUnit.get(), unit.Bot)) {
            result.placeValid = false;
            result.moveValid = false;

        } else {
            throw new LostException("PushOnUnit");
        }

        result.unit = pushed;

        return result;
    }

    private ActionResult computeAction(String command, Unit unit, String dir1, String dir2) throws LostException {
        if (command.equalsIgnoreCase(Action.MOVE)) {
            return computeMove(unit, dir1, dir2);
        } else if (CAN_PUSH && command.equals(Action.PUSH)) {
            return computePush(unit, dir1, dir2);
        } else {
            throw new LostException("InvalidCommand");
        }
    }

    private List<Action> getLegalActions(Bot Bot) {
        List<Action> actions = new LinkedList<>();
        for (Unit unit : Bot.units) {
            for (Direction dir1 : Direction.values()) {
                for (Direction dir2 : Direction.values()) {

                    try {
                        computeAction(Action.MOVE, unit, dir1.name(), dir2.name());
                        actions.add(new Action(Action.MOVE, unit.index, dir1, dir2));
                    } catch (LostException eMove) {
                    }
                    if (CAN_PUSH) {
                        try {
                            computeAction(Action.PUSH, unit, dir1.name(), dir2.name());
                            actions.add(new Action(Action.PUSH, unit.index, dir1, dir2));
                        } catch (LostException ePush) {
                        }
                    }

                }

            }
        }
        actions.sort((a, b) -> a.toBotString().compareTo(b.toBotString()));
        return actions;
    }
    
    protected void prepare(int round) {
        Bots.stream().forEach(Bot::reset);
    }

    
    private Point getNeighbor(String direction, Point position) {
        return getNeighbor(direction, position, grid.size);
    }

    private Point getNeighbor(String direction, Point position, int size) {
        int x = position.x;
        int y = position.y;
        if (direction.contains("E")) {
            x++;
        } else if (direction.contains("W")) {
            x--;
        }
        if (direction.contains("S")) {
            y++;
        } else if (direction.contains("N")) {
            y--;
        }
        return new Point(x, y);
    }

    protected void play(int BotIdx, String atype,int index,String dir1,String dir2){
        
        Bot Bot = Bots.get(BotIdx);
        Unit unit=Bot.units.get(index);
        ActionResult ar ;
        try {
            ar= computeAction(atype,unit,dir1,dir2);
            unit.did = ar;
            if (ar.moveValid) {
                ar.unit.position = ar.moveTarget;
            }
            if (ar.placeValid) {
                grid.place(ar.placeTarget);
            }
            if (ar.scorePoint) {
                Bot.score++;
            }
            if (ar.type.equals(Action.PUSH)) {
                ar.unit.gotPushed = true;
            }
        }
        catch (LostException e){
            
        }
        
    }

    
    protected void updateGame(int round) {
        for (Unit unit : units) {
            if (WIN_ON_MAX_HEIGHT && grid.get(unit.position).equals(FINAL_HEIGHT - 1)) {
                unit.Bot.win();
            }
        }
    }


    
    protected String[] getBotActions(int BotIdx, int round) {
        return new String[0];
    }

    
    protected int getScore(int BotIdx) {
        Bot p = Bots.get(BotIdx);
        if (WIN_ON_MAX_HEIGHT) {
            if (p.dead)
                return -1;
            if (p.won)
                return 1;
            return 0;
        }
        return p.score;
    }

    private static Grid grid;
    private static List<Bot> Bots;
    private static List<Unit> units;

    public static void main(String args[]) {
        int botsCount=2;
        int myIdx=0,otherIdx=1;
        Pplayer player;
        Scanner in = new Scanner(System.in);
        int size = in.nextInt();
        int unitsPerBot = in.nextInt();
        player.initGame(botsCount,size);
        for(int i=0;i<botsCount;i++){
            player.Bots.add(new Bot(i));   
        }
        for(int i=0;i<botsCount;i++){
            for(int j=0;j<unitsPerBot;j++){
                Unit u=new Unit(player.Bots.get(i),j);
                player.units.add(u); 
                player.Bots.get(i).units.add(u);
            } 
        }

        // game loop
        while (true) {
            for (int i = 0; i < size; i++) {
                player.update(i,in.next());
            }
            for (int i = 0; i < unitsPerBot; i++) {
                int unitX = in.nextInt();
                int unitY = in.nextInt();
                player.Bots.get(myIdx).getsetPosition(new Point(unitX,unitY));
            }
            for (int i = 0; i < unitsPerBot; i++) {
                int otherX = in.nextInt();
                int otherY = in.nextInt();
                player.Bots.get(myIdx).getsetPosition(new Point(otherX,otherY));
            }
            int legalActions = in.nextInt();
            for (int i = 0; i < legalActions; i++) {
                String atype = in.next();
                int index = in.nextInt();
                String dir1 = in.next();
                String dir2 = in.next();
            }
            for(Bot b : player.Bots){
                System.err.println("Debug messages..."+player.getLegalActions(b));
            }
            System.out.println("MOVE&BUILD 0 N S");
        }
    }
}