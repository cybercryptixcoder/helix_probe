import re

# ---------------------------------------------------------------------------
# What the box seems to be (level 1):
#
# BACKGROUND / STATIC SCENE
#  - Most cells are '5' (background). Static decorations in 0/2/3/f.
#
# THE COUNTER (row 63)
#  - r63 is a progress counter.  A click on an "active" cell advances the
#    counter by writing '5' into the next cell of r63, moving leftwards.
#    The next free cell is the leftmost cell of the trailing run of '5'
#    that starts at c63 (i.e. the cursor marches leftward from c63).
#  - Which clicks are "active"?  A click advances the counter iff the
#    clicked cell is currently '0' (a button/hole).  Clicks on '5'
#    background or on 'f'/'2'/'3' decoration do nothing. [E11,E16,E20,E22,
#    E24: clicks on 5 do nothing; clicks on 0 advance]
#  - The switch cells (43,4)/(37,4)/(41,4) ALSO advance the counter when
#    they toggle [E1,E3,E5,E6,E13,E14,E15,E17,E25].
#
# SWITCHES (toggling regions)
#  - CLICK 43 4 / 37 4 / 41 4 toggle a 5-wide x 5-tall block at r7 c35-45
#    between pattern A (c35-39:0, c41-45:3) and pattern B (c35-39:3,
#    c41-45:0).  They ALSO toggle a big block at r33-44 c39-45 between 0
#    and f.  [E15,E17,E25: the big block is at r33-44 c39-45, NOT r25-31
#    c26-37 as v16 had it.]
#
# ACTIONS
#  - ACTION1..5 paint a large sprite at a location that depends on the
#    current state (the sprite appears to be a "reveal" of a hidden shape).
#    ACTION1 painted a sprite around r21-37 c14-28 in E26.  ACTION3 painted
#    a sprite around r40-54 c14-38 in E19.  These are complex and
#    state-dependent; I cannot model them precisely.  Best guess: ACTIONn
#    paints a fixed sprite relative to the current counter position, but
#    the exact shape is unknown.  I'll model ACTIONn as a no-op on the
#    counter (E27: ACTION1 did nothing at all when counter was at c8;
#    E23: ACTION3 did nothing at all).  Actually E26 ACTION1 painted a
#    sprite AND did not advance counter; E27 ACTION1 did nothing.  So
#    ACTIONn paints a sprite only under some condition (maybe when the
#    counter is in a certain range, or when a hidden shape is present).
#    I'll model ACTIONn as: no counter change, and paint nothing (best
#    guess given E27/E23).  Mark "?".
#
# GOAL (guess, marked "?"):
#   The counter fills r63 leftward from c63.  It has reached c8 (E24) and
#   then c7,c6,c5,c4 (E25).  The level likely completes when the counter
#   reaches c0 (left edge), i.e. when r63 c0..c63 are all '5'.  But E25
#   showed clicks at c7,c6,c5,c4 and then c3,c2,c1,c0 would be next; the
#   plan predicted WIN at c0 but the box did NOT win (E25 only got to c4
#   before budget ran out).  Actually E25 ran 6 actions and reached c4.
#   The counter is now at c8 (after E24) then E25 advanced to c4, E26
#   ACTION1 (no counter change), E27 ACTION1 (nothing).  So counter is at
#   c4 now.  Best guess: WIN when r63 c0..c63 all '5' (counter reaches c0).
#   Mark "?".
# ---------------------------------------------------------------------------

COUNTER_ROW = 63

def _grid(frame):
    return [list(row) for row in frame]

def _counter_next_col(grid):
    # The counter fills from c63 leftward.  The next free cell is the
    # leftmost cell of the trailing run of '5' starting at c63.
    row = grid[COUNTER_ROW]
    c = 63
    while c >= 0 and row[c] == '5':
        c -= 1
    # c now points at first non-5 (or -1).  next free is c (if >=0)
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
            # "?" It may paint a sprite under some conditions (E19, E26).
            pass
        elif act == "RESET":
            pass

        # goal check (guess): counter filled all of r63
        row = grid[COUNTER_ROW]
        filled = all(row[c] == '5' for c in range(0, 64))
        if filled and state == "NOT_FINISHED":
            state = "WIN"
            levels = 1

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
