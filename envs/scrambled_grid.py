"""A game with scrambled controls: a character on a 9x9 board and five unlabeled buttons.

The experimenter is told nothing about what the buttons do. Hidden rules (don't show these to it):
    A  up 1
    B  right 2, one cell at a time (stops early at a wall or the edge)
    C  left 1
    D  down 1, but down 2 in the upper half of the board (y >= 5)
    E  swaps x and y (a jump across the diagonal), unless the landing cell is a wall
    walls at (3,3) (3,4) (6,2) (5,6) (1,7); the board edge also blocks
Goals: get from one cell to another in at most 8 presses.
"""
from probe.env import Environment, Task

N = 9
WALLS = {(3, 3), (3, 4), (6, 2), (5, 6), (1, 7)}
BUTTONS = "ABCDE"


def free(x, y):
    return 0 <= x < N and 0 <= y < N and (x, y) not in WALLS


def step(x, y, b):
    if b == "E":
        return (y, x) if free(y, x) else (x, y)
    dx, dy, n = {"A": (0, 1, 1), "B": (1, 0, 2), "C": (-1, 0, 1), "D": (0, -1, 2 if y >= 5 else 1)}[b]
    for _ in range(n):
        if not free(x + dx, y + dy):
            break
        x, y = x + dx, y + dy
    return x, y


class ScrambledGrid(Environment):
    name = "scrambled_grid"
    brief = """A small video game. A character stands on a 9x9 board; cells are (x, y) with x and y from 0 to 8, \
(0, 0) at the bottom-left, x growing to the right and y growing upward. There are five buttons, A B C D E. Nobody \
has told you what they do. In one experiment you place the character on any cell you like, press a sequence of \
buttons, and see where the character is after each press. The game is deterministic."""
    probe_format = """probe:       {"start": [x, y], "presses": "ABCD"}   (1 to 8 presses, letters A-E)
observation: {"start": [x, y], "path": [[x, y], ...]}   (the position after each press, one per press)
If the start cell can't be stood on, the probe is rejected with an error."""
    knowledge = """Tip from a previous player: some cells are walls, and the character can't enter them or stand on \
them. At least one button doesn't move the character the same way everywhere on the board."""

    def validate(self, p):
        s, presses = p.get("start"), p.get("presses")
        if not (isinstance(s, list) and len(s) == 2 and all(isinstance(v, int) for v in s)):
            return 'start must be [x, y] with integers'
        if not free(*s):
            return f"the character can't stand on {s} (off the board or a wall)"
        if not (isinstance(presses, str) and 1 <= len(presses) <= 8 and set(presses) <= set(BUTTONS)):
            return "presses must be a string of 1 to 8 letters from ABCDE"
        return None

    def probe(self, p):
        x, y = p["start"]
        path = []
        for b in p["presses"]:
            x, y = step(x, y, b)
            path.append([x, y])
        return {"start": list(p["start"]), "path": path}

    def random_probe(self, rng):
        cells = [(x, y) for x in range(N) for y in range(N) if free(x, y)]
        x, y = rng.choice(cells)
        return {"start": [x, y], "presses": "".join(rng.choice(BUTTONS) for _ in range(rng.randint(1, 8)))}

    def make_tasks(self, rng, n):
        cells = [(x, y) for x in range(N) for y in range(N) if free(x, y)]
        tasks = []
        while len(tasks) < n:
            s, t = rng.choice(cells), rng.choice(cells)
            d = shortest(s, t)
            if d is None or not 3 <= d <= 8:
                continue
            tasks.append(Task(f"Get the character from {list(s)} to {list(t)} in at most 8 presses. Your probe's "
                              f"start must be {list(s)}; the goal is reached if the character ends on {list(t)}.",
                              lambda o, s=s, t=t: o["start"] == list(s) and o["path"][-1] == list(t)))
        return tasks


def shortest(s, t):
    frontier, seen = [s], {s: 0}
    while frontier:
        nxt = []
        for c in frontier:
            for b in BUTTONS:
                d = step(*c, b)
                if d not in seen:
                    seen[d] = seen[c] + 1
                    nxt.append(d)
        frontier = nxt
    return seen.get(t)
