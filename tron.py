import sys
import time


def err(*args):
    sys.stderr.write(', '.join([str(arg) for arg in args]) + "\n")


def move_to_dir(old, new):
    if old[0] < new[0]:
        return "RIGHT"
    if old[1] < new[1]:
        return "DOWN"
    if old[0] > new[0]:
        return "LEFT"
    return "UP"


class Board():

    def __init__(self, board):
        self.board = board

    def show(self):
        return "\n".join([' '.join(map(str, x)) for x in self.board])


def get_score(starts):
    t1 = time.time()
    graphs = {i: {} for i in range(n_players)}
    graphset = set(x for x in occupied)
    order = list(range(my_id, n_players)) + list(range(0, my_id))
    # err("order order", order)
    it = 1
    board = [['.' for j in range(30)] for i in range(20)]
    while True:
        full = True
        moves = {}
        for o in order:
            for x in starts[o]:
                for n in NEIGHBOURS[x]:
                    if n not in graphset or (n in moves and it == 1):
                        full = False
                        graphset.add(n)
                        moves[n] = o
        for k, v in moves.items():
            graphs[v][k] = it
            board[k[1]][k[0]] = v
        if full:
            break
        starts = [[k for k, v in moves.items() if v == i] for i in range(n_players)]
        it += 1
    num_my_tiles = len(graphs[my_id])
    num_enemy_tiles = sum([len(graphs[i]) for i in range(n_players) if i != my_id])
    enemies_dist = sum([sum(graphs[i].values()) for i in range(n_players) if i != my_id])
    # err("t", time.time() - t1)
    return sum([num_my_tiles * 10000000, num_enemy_tiles * -100000, enemies_dist]), Board(board)

NEIGHBOURS = {}
for i in range(30):
    for j in range(20):
        neighbours = []
        if i < 29:
            neighbours.append((i + 1, j))
        if i > 0:
            neighbours.append((i - 1, j))
        if j < 19:
            neighbours.append((i, j + 1))
        if j > 0:
            neighbours.append((i, j - 1))
        NEIGHBOURS[(i, j)] = neighbours

occupied = {}
while True:
    n_players, my_id = [int(i) for i in input().split()]
    curr_moves = []
    for i in range(n_players):
        x0, y0, x1, y1 = [int(j) for j in input().split()]
        occupied[(x0, y0)] = i
        occupied[(x1, y1)] = i
        curr_moves.append((x1, y1))
    for i, cm in enumerate(curr_moves):
        if cm == (-1, -1):
            occupied = {k: v for k, v in occupied.items() if v != i}
    for p in range(n_players):
        x1, y1 = curr_moves[p]
        if p == my_id:
            me = (x1, y1)
            scores = []
            # err("me", me)
            # err("neg", NEIGHBOURS[me])
            for neighbour in NEIGHBOURS[me]:
                if neighbour not in occupied:
                    player_starts = [[x] for x in curr_moves.copy()]
                    player_starts[my_id] = [neighbour]
                    # err("player_starts", player_starts)
                    for i, cm in enumerate(curr_moves):
                        if cm == (-1, -1):
                            player_starts[i] = []
                    score, brd = get_score(player_starts)
                    scores.append((score, brd, neighbour))
    best_score_move = sorted(scores, key=lambda x: x[0], reverse=True)[0]
    # err("scoring", scores)
    # err("best", best_score_move)
    # err("board")
    # err(best_score_move[1].show())
    print(move_to_dir(me, best_score_move[-1]))
