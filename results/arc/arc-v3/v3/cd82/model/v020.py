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
#  - E29: filling c0 (the last cell) triggers GAME_OVER, not WIN. So
#    filling the counter to c0 is a LOSS. The counter must NOT reach c0.
#    [E29: CLICK 43 4 wrote r63 c0:5 and state became GAME_OVER]
#
# SWITCHES (toggling regions)
#  - CLICK 43 4 / 37 4 / 41 4 toggle a 5-wide x 5-tall block at r7 c35-45
#    between pattern A (c35-39:0, c41-45:3) and pattern B (c35-39:3,
#    c41-45:0). They ALSO toggle a big block at r33-44 c39-45 between 0
#    and f. [E15,E17,E25]
#
# ACTIONS (paint sprites)
#  - ACTIONn paints a sprite at a fixed location, but ONLY when the
#    counter is at a particular position (a "gate"). E26: ACTION1 painted
#    a big sprite (r21-37 c14-28) when counter was at c19. E27: ACTION1
#    did nothing when counter was at c8 (after E26's fill). E19: ACTION3
#    painted (r40-54 c14-38) when counter was at c24. E18: ACTION3
#    painted (r40-54 c25-49) when counter was at c27. E23: ACTION3 did
#    nothing (counter at c21?). E31: ACTION5 painted (r34-38 c27-36) when
#    counter was at c63 (fresh). So each ACTION paints only when the
#    counter is in a specific range/state. Best guess "?": ACTIONn paints
#    iff the counter's next-free column is in some window; we don't know
#    the exact windows, so we model ACTIONn as painting iff the counter
#    is NOT full and NOT at the "wrong" spot. This is very uncertain.
#    Simplification "?": ACTIONn paints iff counter next-free col is
#    between 15 and 40 (E26 c19 yes, E19 c24 yes, E18 c27 yes, E27 c8 no,
#    E23 c21 no — contradicts). So the gate is not a simple range.
#    Given the contradictions, model ACTIONn as: paints a fixed sprite
#    (per n) iff the counter's next-free column equals a specific value
#    observed for that action. Mark "?".
#
# GOAL (guess, marked "?"):
#   Filling c0 causes GAME_OVER (E29). So the counter must NOT be filled
#   to c0. The counter fills c63..c1 (63 cells) without winning (E28).
#   Best guess: the level completes when the counter is full (c1..c63
#   all '5', c0 still '4') AND some ACTION paints the right sprite, or
#   when a specific ACTION is pressed at the right counter position.
#   Given E26 (ACTION1 at c19 painted a big sprite) and no win, and E19
#   (ACTION3 at c24) no win, the win likely needs a specific ACTION at a
#   specific counter position. I'll guess: WIN when an ACTION paints a
#   sprite AND the counter is in a "goal" window. Since I can't pin it,
#   I'll guess WIN when ACTION1 is pressed with counter next-free col in
#   [15,25] (E26 was c19, no win though). Mark "?" strongly.
#   Alternative guess: the goal is to fill the counter to exactly c1
#   (63 cells) and then press a specific ACTION. E28 filled to c1 with
#   no win, so that alone isn't it. I'll guess: WIN when counter is full
#   (c1..c63 all 5) AND ACTION1 is pressed. Mark "?".
# ---------------------------------------------------------------------------

COUNTER_ROW = 63

def _grid(frame):
    return [list(row) for row in frame]

def _counter_next_col(grid):
    row = grid[COUNTER_ROW]
    c = 63
    while c >= 0 and row[c] == '5':
        c -= 1
    return c if c >= 0 else None

def _counter_full(grid):
    row = grid[COUNTER_ROW]
    return all(row[c] == '5' for c in range(1, 64))

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
                if (x, y) in ((43, 4), (37, 4), (41, 4)):
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
                    blk = grid[33][39]
                    newv = 'f' if blk == '0' else '0'
                    for r in range(33, 45):
                        for c in range(39, 46):
                            if grid[r][c] != newv:
                                changes[f"{r},{c}"] = newv
                                grid[r][c] = newv
                    nxt = _counter_next_col(grid)
                    if nxt is not None:
                        changes[f"{COUNTER_ROW},{nxt}"] = '5'
                        grid[COUNTER_ROW][nxt] = '5'
                        # E29: filling c0 => GAME_OVER
                        if nxt == 0:
                            state = "GAME_OVER"
                elif cur == '0':
                    nxt = _counter_next_col(grid)
                    if nxt is not None:
                        changes[f"{COUNTER_ROW},{nxt}"] = '5'
                        grid[COUNTER_ROW][nxt] = '5'
                        if nxt == 0:
                            state = "GAME_OVER"
        elif act.startswith("ACTION"):
            # ACTIONn paints a sprite iff counter next-free col matches
            # a per-action gate. Best guess "?":
            #  ACTION1: gate col 19 (E26 painted, E27 at c8 no)
            #  ACTION3: gate col 24 (E19) and 27 (E18); no at c21 (E23)
            #  ACTION5: gate col 63 (E31 fresh)
            # We model: paint iff next-free col is in the observed set
            # for that action. This is a guess.
            nxt = _counter_next_col(grid)
            m = re.match(r"ACTION(\d+)", act)
            n = int(m.group(1)) if m else 0
            gates = {1: {19}, 3: {24, 27}, 5: {63}}
            if nxt is not None and nxt in gates.get(n, set()):
                # paint a fixed sprite per action (approx from E26/E19/E31)
                if n == 1:
                    # sprite around r21-37 c14-28 (approx)
                    for r in range(21, 38):
                        for c in range(14, 29):
                            if grid[r][c] != '2':
                                changes[f"{r},{c}"] = '2'
                                grid[r][c] = '2'
                elif n == 3:
                    for r in range(40, 55):
                        for c in range(14, 39):
                            if grid[r][c] != '2':
                                changes[f"{r},{c}"] = '2'
                                grid[r][c] = '2'
                elif n == 5:
                    for r in range(34, 39):
                        for c in range(27, 37):
                            if grid[r][c] != 'f':
                                changes[f"{r},{c}"] = 'f'
                                grid[r][c] = 'f'
                # goal guess "?": counter full AND ACTION1 pressed
                if _counter_full(grid) and n == 1 and state == "NOT_FINISHED":
                    state = "WIN"
                    levels = 1
        elif act == "RESET":
            pass

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
