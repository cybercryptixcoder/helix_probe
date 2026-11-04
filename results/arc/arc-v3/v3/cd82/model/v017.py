import re

# ---------------------------------------------------------------------------
# What the box seems to be (level 1, "after 88 actions"):
#
# BACKGROUND / STATIC SCENE
#  - The screen is a 64x64 hex grid. Most cells are '5' (background).
#  - There are static decorative objects (rectangles) drawn in 0/2/3/f.
#    Clicking a "clickable object" that is a *switch* toggles a region.
#
# THE COUNTER (bottom row)
#  - r63 is a progress/counter row.  A click on an "active" cell advances a
#    counter by writing '5' into the next cell of r63, moving leftwards
#    (c63, c62, c61, ... c10, c9, c8 ...).  [E1,E2,E4,E6,E8,E9,E10,E12,
#    E13,E14,E15,E16,E20,E21,E22,E23,E24]
#  - Clicks on cells that are NOT active do nothing (0 changes).
#    Which clicks are active?  A click advances the counter iff the clicked
#    cell is '0' (a "button"/hole) or a specific switch.  Clicks on '5'
#    background or on 'f'/'2'/'3' decoration do nothing. [E11,E16,E24 no-op
#    clicks on 5; E1 CLICK 43 4 toggles instead]
#  - So: clicking any '0' cell (or the switch) advances the counter.
#
# SWITCHES (toggling regions)
#  - CLICK 43 4 / 37 4 / 41 4 toggle a 5-wide x 5-tall block at r7 c35-45
#    between pattern A (c35-39:0, c41-45:3) and pattern B (c35-39:3,
#    c41-45:0), and toggle a big 12x7 block at r25-31 c26-37 between 0 and f.
#    [E1,E3,E5,E6,E13,E14,E15,E17]  These are two linked switches that
#    flip the same region.
#  - CLICK 16 16 also advances counter (it's a '0' cell).
#  - ACTION1..5: ACTION1/2/3/4/5 mostly do nothing visible except that
#    some of them ALSO advance the counter by 1 (like a click on a '0').
#    Looking at evidence: ACTION1 advanced counter [E8, E12, E21];
#    ACTION2 advanced counter [E10, E17]; ACTION3 advanced counter [E18];
#    ACTION4 advanced counter [E9]; ACTION5 did NOT advance [E5,E7].
#    Actually ACTION5 changed the big block [E7].  Hmm.
#
# Given the messiness, the reliable mechanism is:
#   * CLICK on a cell whose current colour is '0'  -> counter advances
#     (write '5' at the next free counter cell, scanning r63 right-to-left).
#   * CLICK on the switch cells (43,4)/(37,4)/(41,4) -> toggle the two
#     linked blocks (r7 c35-45 pattern and r25-31 c26-37 0<->f).
#   * CLICK elsewhere -> nothing.
#   * ACTIONn -> advances counter by 1 (best guess; ACTION5 maybe toggles).
#
# GOAL (guess, marked "?"):
#   The counter is filling r63 from the right.  The level likely completes
#   when the counter reaches a target column (e.g. c0 / left edge), i.e.
#   when the whole bottom row fills, OR when the big f-block is fully
#   revealed.  Best guess: filling r63 leftwards to some threshold.
#   I'll predict WIN when r63 becomes fully '5' left of c8 (i.e. c8..c63
#   all '5'), since the counter has been marching steadily left.
# ---------------------------------------------------------------------------

COUNTER_ROW = 63

def _grid(frame):
    return [list(row) for row in frame]

def _counter_next_col(grid):
    # find leftmost '5' run start: the counter fills from right to left.
    # next cell to fill is the rightmost cell in r63 that is still '5'
    # among the filled span.  Simplest: rightmost '5' in r63 that has a
    # non-'5' to its right OR is at c63.
    row = grid[COUNTER_ROW]
    # filled cells are '5'; but background is also '5'.  The counter cells
    # are the contiguous '5's at the right end.  Find rightmost non-5 in
    # row; counter grows leftward from c63.  Track by counting '5's from
    # the right that were written.  We approximate: the next free cell is
    # the rightmost '5' such that everything to its right is '5' and it is
    # within the counter span (c8..c63).
    for c in range(63, 7, -1):
        if row[c] == '5':
            # check it's the leftmost of the trailing run?  Actually the
            # counter writes progressively leftward, so the leftmost '5'
            # of the trailing run is next.
            pass
    # leftmost cell of the trailing run of '5' in c8..c63
    c = 63
    while c >= 8 and row[c] == '5':
        c -= 1
    # c now points at first non-5 (or 7).  next free is c (if >=8)
    return c if c >= 8 else None

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
                # switch cells toggle linked blocks
                if (x, y) in ((43, 4), (37, 4), (41, 4)):
                    # toggle r7 c35-45 pattern
                    row7 = grid[7]
                    # pattern A: c35-39=0, c41-45=3 ; B: c35-39=3,c41-45=0
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
                    # toggle big block r25-31 c26-37 between 0 and f
                    blk = grid[25][26]
                    newv = 'f' if blk == '0' else '0'
                    for r in range(25, 32):
                        for c in range(26, 38):
                            if grid[r][c] != newv:
                                changes[f"{r},{c}"] = newv
                                grid[r][c] = newv
                    # switch click also advances counter (E1: 43 4 advanced)
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
            # ACTIONn advances counter by 1 (best guess)
            nxt = _counter_next_col(grid)
            if nxt is not None:
                changes[f"{COUNTER_ROW},{nxt}"] = '5'
                grid[COUNTER_ROW][nxt] = '5'
        elif act == "RESET":
            # restart level: not modelled precisely
            pass

        # goal check (guess): counter filled up to c8
        row = grid[COUNTER_ROW]
        filled = all(row[c] == '5' for c in range(8, 64))
        if filled and state == "NOT_FINISHED":
            state = "WIN"
            levels = 1

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
