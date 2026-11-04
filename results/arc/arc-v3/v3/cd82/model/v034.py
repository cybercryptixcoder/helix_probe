import re

# ---------------------------------------------------------------------------
# MODEL OF THE BOX (level 1)  -- v34
#
# Beliefs:
#  - Background is colour 5. Row 63 is a counter bar filled from the RIGHT
#    (c63 first) leftwards, one cell -> '5' per "point" [E1..E6, E30, E64].
#  - A point is awarded ONLY when an action produces a visible change
#    (>=1 cell changes). Actions that change nothing award no point
#    [E68: 2nd ACTION2 no change -> no point; E73: ACTION1 no change -> no
#    point; E71: CLICK 32 28 no change -> no point; E72: CLICK 32 28 DID
#    change -> point].
#  - CLICK on a plain background '5' cell does NOTHING: no change, no point
#    [E11,E16,E22,E48,E59,E60,E63,E64,E67,E71].
#  - ACTION1..5 move/draw a '2/f' sprite and a big 'f' block in the maze;
#    when the sprite is already at its limit the action is a no-op (no point)
#    [E68, E73]. Exact sprite motion is not modelled; we approximate.
#  - CLICK on a maze cell toggles a rectangular region between 0 and f
#    [E61,E62,E65,E66]. Exact region uncertain.
#  - RESET restores the level-1 initial screen [E30,E65,E66,E70].
#  - When the bar reaches c0 (64th point) the game goes GAME_OVER [E29,E64].
#
# What completes level 1:  (best guess, marked "?")
#  Unknown. predict() never claims WIN (reports NOT_FINISHED / GAME_OVER).
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

def _toggle_rect(grid, x, y, changes):
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
            return changes
        _toggle_rect(grid, x, y, changes)
        if changes:
            _advance_bar(grid, changes)
        return changes
    if act.startswith('ACTION'):
        # We do not model sprite motion precisely. Heuristic: assume the
        # action changes something (and thus awards a point) unless the
        # sprite is already at a limit. Without sprite tracking we assume
        # it changes -> point. This over-predicts but is our best guess.
        # ? (unproven: exact no-op condition)
        _advance_bar(grid, changes)
        return changes
    if act == 'RESET':
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
