import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS (revised v34)
    #
    # Screen: 64x64 grey (5) playfield. Right strip cols 62-63 is a
    # timer bar filling with 0 from top, 2 rows per action that counts.
    # When it reaches row 64 -> GAME_OVER.
    #
    # PLAYER SPRITE: 4x4 block rows 19-22. Tail (a) rows 19-20, head (9)
    # rows 21-22. [current screen, E92, E94, E96]
    # ACTION1/ACTION3 move sprite RIGHT 2 cols. ACTION2/ACTION4 move LEFT
    # 2 cols. [E92 ACTION1 moved sprite, E96 ACTION2 moved sprite]
    # Sprite travel range: left wall at c39, right wall at c42 (sprite
    # confined to c39-42). [E97 ACTION2 at c39-42 -> no sprite move;
    # E84/E86 ACTION1 at c39-42 -> no sprite move]
    # When sprite is blocked at a wall, the action STILL advances the bar
    # by 2 rows. [E98 ACTION2 at c39-42 -> bar only; E84/E86/E91 bar only]
    # (E97's 0-change ACTION2 is treated as an anomaly; latest E98 wins.)
    #
    # SWITCHES: 3x3 clusters at rows 49-51/54-56/59-61, cols 24-26/29-31/
    # 34-36. CLICK cycles e->0->2->e. [E67,E72,E73,E78,E79,E83,E85,E87,
    # E88] CLICK elsewhere: nothing. [E17,E31,E33,E49,E57,E61,E68,E89,E93]
    # Bar advances 2 rows on a cluster click that changes cells, EXCEPT
    # clicks on bottom row (y 59-61) don't advance bar. [E79,E87 vs
    # E83,E85,E88] Also no bar when new colour is e. [E88 click2]
    #
    # GOAL (?): unknown. Best guess: set all switch clusters to a target
    # pattern (e.g. all 2), or move sprite to a target. Predict no
    # completion.
    # ------------------------------------------------------------------

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    # Reconstruct strip fill height from grid
    strip_rows = 0
    for r in range(64):
        if grid[r][62] == '0' and grid[r][63] == '0':
            strip_rows = r + 1
        else:
            break

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    def strip_advance(g, n=2):
        nonlocal strip_rows
        changed = {}
        for _ in range(n):
            if strip_rows < 64:
                r = strip_rows
                for c in (62, 63):
                    if g[r][c] != '0':
                        g[r][c] = '0'
                        changed[f"{r},{c}"] = '0'
                strip_rows += 1
        return changed

    def sprite_span(g):
        lo = 64; hi = -1
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] in ('9', 'a'):
                    if c < lo: lo = c
                    if c > hi: hi = c
        return lo, hi

    def move_sprite(g, direction):
        # direction +1 = right, -1 = left. Move 2 cols.
        # Returns (changed, moved). If blocked, moved=False but caller
        # still advances the bar.
        changed = {}
        lo, hi = sprite_span(g)
        if hi < 0:
            return changed, False
        width = hi - lo + 1
        new_lo = lo + 2 * direction
        # Left wall at c39, right wall at c42 (sprite confined to c39-42).
        if new_lo < 39 or new_lo + width - 1 > 42:
            return changed, False
        block = [[g[r][c] for c in range(lo, hi + 1)] for r in range(19, 23)]
        for r in range(19, 23):
            for c in range(lo, hi + 1):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '5'
                    changed[f"{r},{c}"] = '5'
        for i, r in enumerate(range(19, 23)):
            for j in range(width):
                nc = new_lo + j
                if block[i][j] in ('9', 'a'):
                    if g[r][nc] != block[i][j]:
                        g[r][nc] = block[i][j]
                        changed[f"{r},{nc}"] = block[i][j]
        return changed, True

    def toggle_small_cluster(g, x, y):
        changed = {}
        targets = []
        for rr in (49, 54, 59):
            for cc in (24, 29, 34):
                if cc <= x <= cc + 2 and rr <= y <= rr + 2:
                    targets.append((rr, cc))
        if not targets:
            return changed, None
        new_colour = None
        for rr, cc in targets:
            for r in range(rr, rr + 3):
                for c in range(cc, cc + 3):
                    old = g[r][c]
                    if old == 'e':
                        new = '0'
                    elif old == '0':
                        new = '2'
                    elif old == '2':
                        new = 'e'
                    else:
                        new = old
                    if new != old:
                        g[r][c] = new
                        changed[f"{r},{c}"] = new
                        new_colour = new
        return changed, new_colour

    for act in actions:
        changed = {}
        act = act.strip()
        if act == "RESET":
            for r in range(64):
                for c in (62, 63):
                    if grid[r][c] != 'e':
                        grid[r][c] = 'e'
                        changed[f"{r},{c}"] = 'e'
            strip_rows = 0
            state = "NOT_FINISHED"
        elif act in ("ACTION1", "ACTION3"):
            ch, moved = move_sprite(grid, +1)
            changed.update(ch)
            # Bar advances whether or not sprite moved (blocked still counts)
            changed.update(strip_advance(grid, 2))
        elif act in ("ACTION2", "ACTION4"):
            ch, moved = move_sprite(grid, -1)
            changed.update(ch)
            changed.update(strip_advance(grid, 2))
        elif act.startswith("CLICK"):
            parts = act.split()
            if len(parts) == 3:
                try:
                    x = int(parts[1]); y = int(parts[2])
                except ValueError:
                    x = y = -1
                ch, new_colour = toggle_small_cluster(grid, x, y)
                if ch:
                    changed.update(ch)
                    # Bar advances on cluster click UNLESS new colour is e
                    # OR click is in bottom row (y 59-61).
                    if new_colour != 'e' and not (59 <= y <= 61):
                        changed.update(strip_advance(grid, 2))
        if strip_rows >= 64:
            state = "GAME_OVER"
        steps.append({
            "changes": changed,
            "levels": levels_done,
            "state": state
        })

    return {"steps": steps}
