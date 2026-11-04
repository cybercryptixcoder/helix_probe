import re

# ---------------------------------------------------------------------------
# MODEL OF THE BOX (level 1)  -- v33
#
# Beliefs (each line cites evidence):
#  - Background is colour 5. Row 63 is a counter bar: it fills from the RIGHT
#    (c63 first) leftwards, one cell -> '5' per "point" [E1..E6, E30, E64].
#  - A point is awarded per accepted action: every ACTIONn and every CLICK
#    that lands on a non-background cell (colour != '5') [E1,E3,E5,E7,E8,E68].
#  - CLICK on a plain background '5' cell does NOTHING: no point, no change
#    [E11,E16,E22,E48,E59,E60,E63,E64,E67,E71].
#  - ACTION2 is inert visually but still awards a point [E68,E71].
#  - ACTION4/ACTION5/ACTION1/ACTION3 draw/move a '2/f' sprite and a big 'f'
#    block in the maze; these are cosmetic w.r.t. the counter [E69,E65,E66].
#  - CLICK on a maze cell toggles a rectangular region between 0 and f
#    [E61,E62,E65,E66]. Exact region is uncertain; we model a modest rect.
#  - RESET restores the level-1 initial screen (counter cleared, sprite and
#    toggles back to start) [E30,E65,E66,E70].
#  - When the bar reaches c0 (64th point) the game goes GAME_OVER [E29,E64].
#
# What completes level 1:  (best guess, marked "?")
#  Unknown. The bar is a lives/energy meter that must NOT be emptied. The
#  most plausible goal is moving the sprite onto a goal region in the maze,
#  but no experiment has reached it. predict() therefore never claims WIN
#  (reports NOT_FINISHED / GAME_OVER only) -- a wrong WIN guess is costly.
#  ? (unproven)
# ---------------------------------------------------------------------------

def _parse(frame):
    return [list(r) for r in frame]

def _bar_count(grid):
    n = 0
    for c in range(63, -1, -1):
        if grid[63][c] == '5':
            n += 1
        else:
            break
    return n

def _advance_bar(grid, changes):
    for c in range(63, -1, -1):
        if grid[63][c] != '5':
            grid[63][c] = '5'
            changes[(63, c)] = '5'
            return
    # already full

def _toggle_rect(grid, x, y, changes):
    """Toggle a rectangle between 0 and f around (x,y)."""
    h, w = len(grid), len(grid[0])
    r0, r1 = max(0, y - 6), min(h - 1, y + 5)
    c0, c1 = max(0, x - 3), min(w - 1, x + 3)
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            cur = grid[r][c]
            if cur == '0':
                grid[r][c] = 'f'
                changes[(r, c)] = 'f'
            elif cur == 'f':
                grid[r][c] = '0'
                changes[(r, c)] = '0'

def _step(grid, act):
    changes = {}
    m = re.match(r'CLICK\s+(\d+)\s+(\d+)', act)
    if m:
        x, y = int(m.group(1)), int(m.group(2))
        h, w = len(grid), len(grid[0])
        if not (0 <= y < h and 0 <= x < w):
            return changes
        if grid[y][x] == '5':
            # background click: inert, no point
            return changes
        # non-background: toggle region and award a point
        _toggle_rect(grid, x, y, changes)
        _advance_bar(grid, changes)
        return changes
    if act.startswith('ACTION'):
        # cosmetic sprite movement not modelled; just a point
        _advance_bar(grid, changes)
        return changes
    if act == 'RESET':
        # approximate: clear the bar (restore initial). We don't know the
        # exact initial screen, so only clear row 63.
        for c in range(64):
            if grid[63][c] == '5':
                grid[63][c] = '4'
                changes[(63, c)] = '4'
        return changes
    return changes

def predict(probe):
    try:
        frame = probe.get('frame')
        level = probe.get('level', 0)
        history = probe.get('history', [])
        actions = probe.get('actions', [])
        if frame is None:
            return {'steps': [{'changes': {}, 'levels': level,
                               'state': 'NOT_FINISHED'} for _ in actions]}
        grid = _parse(frame)
        for act in history:
            _step(grid, act)
        steps = []
        for act in actions:
            changes = _step(grid, act)
            bar = _bar_count(grid)
            state = 'NOT_FINISHED'
            if bar >= 64:
                state = 'GAME_OVER'
            steps.append({
                'changes': {f'{r},{c}': v for (r, c), v in changes.items()},
                'levels': level,
                'state': state,
            })
            if state == 'GAME_OVER':
                break
        return {'steps': steps}
    except Exception:
        n = len(probe.get('actions', []))
        lv = probe.get('level', 0)
        return {'steps': [{'changes': {}, 'levels': lv,
                           'state': 'NOT_FINISHED'} for _ in range(n)]}
