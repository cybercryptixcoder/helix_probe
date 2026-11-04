import re

# ---------------------------------------------------------------------------
# What the box seems to be (level 1):
#
# BACKGROUND / STATIC SCENE
#  - Most cells are '5' (background). Static decorations in 0/2/3/f.
#
# THE COUNTER (row 63)
#  - r63 is a progress counter. A click on an "active" cell advances the
#    counter by writing '5' into the next cell of r63, moving leftwards.
#    The next free cell is the leftmost cell of the trailing run of '5'
#    that starts at c63 (cursor marches leftward from c63).
#  - Which clicks are "active"? A click advances the counter iff the
#    clicked cell is currently '0' (a button/hole). Clicks on '5'
#    background or on 'f'/'2'/'3' decoration do nothing. [E11,E16,E20,E22,
#    E24: clicks on 5 do nothing; clicks on 0 advance]
#  - The switch cells (43,4)/(37,4)/(41,4) ALSO advance the counter when
#    they toggle [E1,E3,E5,E6,E13,E14,E15,E17,E25].
#
# SWITCHES (toggling regions)
#  - CLICK 43 4 / 37 4 / 41 4 toggle a 5-wide x 5-tall block at r7 c35-45
#    between pattern A (c35-39:0, c41-45:3) and pattern B (c35-39:3,
#    c41-45:0). They ALSO toggle a big block at r33-44 c39-45 between 0
#    and f. [E15,E17,E25]
#
# ACTIONS
#  - ACTIONn paint a sprite. ACTION1 painted a sprite around r21-37
#    c14-28 in E26. ACTION3 painted a sprite around r40-54 c14-38 in E19.
#    E27: ACTION1 did nothing when counter was at c8. E23: ACTION3 did
#    nothing. So ACTIONn paints only under some condition. Best guess:
#    ACTIONn is a no-op on the counter and paints nothing (E27/E23).
#    Mark "?".
#
# GOAL (guess, marked "?"):
#   The counter fills r63 leftward from c63. E28 reached c1 (clicks at
#   c2, c1) but the click that would fill c0 did NOTHING (0 cells
#   changed). So the counter does NOT advance past c1: the run of '5'
#   stops at c1, and c0 is a permanent non-'5' cell (it is '4' in the
#   frame: row 63 starts "4555..."). So "all of r63 == '5'" is
#   unreachable. The counter has now filled c1..c63 (63 cells).
#   Best guess: the level completes when the counter reaches its
#   leftmost reachable cell (c1), i.e. when r63 c1..c63 are all '5'.
#   But E28 shows c1 was just filled and NO win fired. So the goal is
#   something else. "?" Perhaps the goal requires clicking a specific
#   object, or the counter must reach a target count, or a switch
#   combination. Given the counter is now full (c1..c63 all '5'), the
#   remaining lever is the switches / ACTIONs. I'll guess the goal is
#   reached by toggling the switch block into a particular pattern, but
#   I have no evidence. I'll keep the "all r63 c1..c63 == '5'" as a
#   NON-goal (it happened, no win) and instead guess: WIN when the
#   counter is full AND a switch click occurs. Mark "?".
# ---------------------------------------------------------------------------

COUNTER_ROW = 63

def _grid(frame):
    return [list(row) for row in frame]

def _counter_next_col(grid):
    # The counter fills from c63 leftward. The next free cell is the
    # leftmost cell of the trailing run of '5' starting at c63.
    row = grid[COUNTER_ROW]
    c = 63
    while c >= 0 and row[c] == '5':
        c -= 1
    # c now points at first non-5 (or -1). next free is c (if >=0)
    return c if c >= 0 else None

def predict(probe):
    frame = probe.get("frame")
    actions = probe.get("actions", [])
    level = probe.get("level", 0)
    history = probe.get("history", [])
    grid = _grid(frame) if frame else [['5']*64 for _ in range(64)]

    steps = []
    levels = 0
    state = "NOT_FINISHED"

    for act in actions:
        changes = {}
        act = act.strip()

        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                x = y = -1
            if 0 <= x < 64 and 0 <= y < 64:
                cur = grid[y][x]
                # switch cells toggle linked blocks AND advance counter
                if (x, y) in ((43, 4), (37, 4), (41, 4)):
                    # toggle r7 c35-45 pattern
                    row7 = grid[7]
                    isA = (row7[35] == '0')
                    newA = '3' if isA else '0'
                    newB = '0' if isA else '3'
                    for c in range(35, 40):
                        if grid[7][c] != newA:
                            changes[f"7,{c}"] = newA
                            grid[7][c] = newA
                    for c in range(41, 46):
                        if grid[7][c] != newB:
                            changes[f"7,{c}"] = newB
                            grid[7][c] = newB
                    # toggle big block r33-44 c39-45 between 0 and f
                    blk = grid[33][39]
                    newv = 'f' if blk == '0' else '0'
                    for r in range(33, 45):
                        for c in range(39, 46):
                            if grid[r][c] != newv:
                                changes[f"{r},{c}"] = newv
                                grid[r][c] = newv
                    # switch click also advances counter
                    nxt = _counter_next_col(grid)
                    if nxt is not None:
                        changes[f"{COUNTER_ROW},{nxt}"] = '5'
                        grid[COUNTER_ROW][nxt] = '5'
                elif cur == '0':
                    # button: advance counter
                    nxt = _counter_next_col(grid)
                    if nxt is not None:
                        changes[f"{COUNTER_ROW},{nxt}"] = '5'
                        grid[COUNTER_ROW][nxt] = '5'
                # else: nothing
        elif act.startswith("ACTION"):
            # ACTIONn: best guess = no visible change (E23, E27).
            pass
        elif act == "RESET":
            pass

        # goal check (guess, "?"): counter full (c1..c63 all '5') AND a
        # switch click just happened. E28 filled c1 with no win, so the
        # plain "full" condition is NOT the goal.
        row = grid[COUNTER_ROW]
        full = all(row[c] == '5' for c in range(1, 64))
        if full and act.startswith("CLICK") and state == "NOT_FINISHED":
            parts = act.split()
            try:
                sx = int(parts[1]); sy = int(parts[2])
            except Exception:
                sx = sy = -1
            if (sx, sy) in ((43, 4), (37, 4), (41, 4)):
                state = "WIN"
                levels = 1

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
