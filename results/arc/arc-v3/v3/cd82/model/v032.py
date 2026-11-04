import re

# ---------------------------------------------------------------------------
# MODEL OF THE BOX (level 1)
#
# What the screen is:
#  - Background is colour 5. There is a big "maze" drawn in colours 2 (walls),
#    f (floor/path) and 0 (gaps). The bottom row (r63) is a progress bar made of
#    5s that fills from the right (c63) leftwards, one cell per "point".
#  - A "cursor"/player is drawn as a small blob; ACTIONs move it around the
#    maze. CLICKs mostly also count as a "move/point" (they advance the bar),
#    but some CLICKs are on the maze and instead toggle a region.
#
# Key observed facts (citations = experiments):
#  - One point per successful action: the bar cell r63 c(63-k) turns to 5 on
#    the (k+1)-th point [E1,E2,E3,E4,E5,E6,...]. Points are monotonic.
#  - When the bar reaches c0 (the 64th point) the game goes GAME_OVER
#    [E29, E64]. So the bar is a "lives/energy" counter that must not be
#    emptied; the level is NOT completed by filling it.
#  - CLICKs on empty background (e.g. 8 10, 50 50, 55 55, 1 1) do nothing
#    [E11,E16,E22,E48]. CLICKs on the maze area DO count as a point and also
#    toggle a rectangular region between 0 and f [E1,E3,E5,E13,E14,E17,...].
#  - ACTION1..ACTION5 mostly each count as one point (bar advances) and also
#    move/re-draw the player blob in the maze [E7,E8,E9,E10,E26,E33,...].
#    ACTION3 in particular toggles a horizontal strip region [E19,E49].
#  - RESET restores the level to its initial screen [E30,E65,E66].
#
# What completes level 1:  (best guess, marked "?")
#  The maze contains a "goal" region. The player blob must be moved onto the
#  goal. The most likely goal is the small 3x3 f-block near the top
#  (rows 3-5, cols 38-40) which is the only isolated f-square and is
#  highlighted in the initial screen. When the player reaches it, levels
#  becomes 1.  ?  (unproven — no experiment has reached it yet.)
#
# Because we cannot be sure, predict() reports the goal when the player blob
# (tracked by replaying history) overlaps that 3x3 block. Otherwise it
# reports NOT_FINISHED and GAME_OVER when the bar is full.
# ---------------------------------------------------------------------------

GOAL_ROWS = range(3, 6)
GOAL_COLS = range(38, 41)

def _parse_screen(frame):
    return [list(row) for row in frame]

def _bar_count(grid):
    # number of 5s filled from the right on row 63
    n = 0
    for c in range(63, -1, -1):
        if grid[63][c] == '5':
            n += 1
        else:
            break
    return n

def _apply_click(grid, x, y):
    """Return dict of changes for a CLICK at (x,y)."""
    changes = {}
    h = len(grid)
    w = len(grid[0])
    if not (0 <= y < h and 0 <= x < w):
        return changes
    col = grid[y][x]
    # Empty background clicks do nothing (colour 5 and not on maze).
    # We treat colour 5 as background. Clicks on non-5 cells toggle a region.
    if col == '5':
        return changes
    # Toggle a rectangle around the click between 0 and f.
    # Observed rectangles are ~7 wide x 12 tall centered on click.
    # Use a fixed size region: rows y-6..y+5, cols x-3..x+3, clipped.
    r0, r1 = max(0, y - 6), min(h - 1, y + 5)
    c0, c1 = max(0, x - 3), min(w - 1, x + 3)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            cur = grid[r][c]
            if cur == '0':
                changes[(r, c)] = 'f'
            elif cur == 'f':
                changes[(r, c)] = '0'
            # leave 2 and 5 alone
    return changes

def _apply_action(grid, action):
    """Return dict of changes for an ACTIONn."""
    changes = {}
    h = len(grid)
    w = len(grid[0])
    if action == 'ACTION3':
        # Toggle a horizontal strip region (seen in E19/E49).
        # Region roughly rows 42-54, cols 17-25.
        for r in range(42, 55):
            for c in range(17, 26):
                if 0 <= r < h and 0 <= c < w:
                    cur = grid[r][c]
                    if cur == '0':
                        changes[(r, c)] = 'f'
                    elif cur == 'f':
                        changes[(r, c)] = '0'
    # Other actions: no reliable region toggle we can model; just a point.
    return changes

def _player_pos(grid):
    # The player blob is drawn in f/2 near the center; we approximate by
    # finding the topmost-leftmost f cell in the maze interior that isn't
    # part of the fixed floor. This is unreliable, so we return None.
    return None

def _replay(probe):
    level = probe.get('level', 0)
    frame = probe.get('frame')
    history = probe.get('history', [])
    actions = probe.get('actions', [])
    if frame is None:
        # Can't simulate without a screen; assume no changes.
        return [{'changes': {}, 'levels': level, 'state': 'NOT_FINISHED'}
                for _ in actions]

    grid = _parse_screen(frame)
    # Replay history to get current grid and bar count.
    for act in history:
        _step(grid, act)

    steps = []
    for act in actions:
        changes = _step(grid, act)
        bar = _bar_count(grid)
        state = 'NOT_FINISHED'
        lv = level
        if bar >= 64:
            state = 'GAME_OVER'
        # Goal: player blob overlaps the 3x3 f-block at rows 3-5, cols 38-40.
        # We approximate: if that block is all f and the bar hasn't overflowed,
        # assume goal reached when the block is f and some action touched it.
        # ? (unproven)
        if state == 'NOT_FINISHED':
            block_f = all(grid[r][c] == 'f'
                          for r in GOAL_ROWS for c in GOAL_COLS)
            if block_f and bar < 64 and len(changes) > 0:
                # Heuristic: reaching the goal block completes the level.
                # Only trigger if an action changed something near it.
                near = any(3 <= r <= 5 and 38 <= c <= 40 for (r, c) in changes)
                if near:
                    lv = level + 1
                    state = 'WIN'
        steps.append({
            'changes': {f'{r},{c}': v for (r, c), v in changes.items()},
            'levels': lv,
            'state': state,
        })
        if state == 'GAME_OVER':
            break
    return steps

def _step(grid, act):
    """Apply one action to grid in place; return changes dict {(r,c):colour}."""
    changes = {}
    m = re.match(r'CLICK\s+(\d+)\s+(\d+)', act)
    if m:
        x, y = int(m.group(1)), int(m.group(2))
        ch = _apply_click(grid, x, y)
        for (r, c), v in ch.items():
            grid[r][c] = v
        changes.update(ch)
        # A click also counts as a point (bar advances) if it was on maze.
        if ch or (0 <= y < len(grid) and 0 <= x < len(grid[0])
                  and grid[y][x] != '5'):
            _advance_bar(grid, changes)
        return changes
    if act.startswith('ACTION'):
        ch = _apply_action(grid, act)
        for (r, c), v in ch.items():
            grid[r][c] = v
        changes.update(ch)
        _advance_bar(grid, changes)
        return changes
    if act == 'RESET':
        # Reset: restore initial screen. We don't know it exactly, so
        # approximate by clearing bar to 0 and leaving grid.
        for c in range(64):
            if grid[63][c] == '5':
                grid[63][c] = '4'
                changes[(63, c)] = '4'
        return changes
    return changes

def _advance_bar(grid, changes):
    # Find first non-5 from the right on row 63 and set to 5.
    for c in range(63, -1, -1):
        if grid[63][c] != '5':
            grid[63][c] = '5'
            changes[(63, c)] = '5'
            return
    # Bar full: stays full.

def predict(probe):
    try:
        steps = _replay(probe)
    except Exception:
        # Never raise.
        n = len(probe.get('actions', []))
        lv = probe.get('level', 0)
        steps = [{'changes': {}, 'levels': lv, 'state': 'NOT_FINISHED'}
                 for _ in range(n)]
    return {'steps': steps}
