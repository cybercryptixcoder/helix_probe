import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS
    #
    # Screen: 64x64, grey (5) playfield. Right strip cols 62-63 is a
    # timer/progress bar that fills with 0 from the top, 2 rows per action
    # that "counts". When it reaches row 63, next action -> GAME_OVER.
    #
    # The "player" is a 4x4 sprite in rows 19-22. It has a 2x2 head (9) on
    # the left and 2x2 tail (a) on the right, with 2s in between.
    # ACTION1/ACTION3 move it RIGHT by 2 columns; ACTION2/ACTION4 move it
    # LEFT by 2 columns. [E60,E62,E64,E69,E70,E74: ACTION1 moves sprite
    # right 2 cols; E71,E75: ACTION4 moves left 2 cols]
    #
    # The bar advances 2 rows per action, capped at 10 rows (rows 0-9).
    # [E74: bar capped, sprite moved; E70: first advanced, second capped]
    # Actually E75 shows bar at r10-11 filled after=18, so cap is NOT 10.
    # The bar advances 2 rows per action up to row 63. E70 second ACTION1
    # gave 0 changes because... sprite was at right edge? No, sprite moved
    # in E74. Let me reconsider: E70 after=6, bar r0-1 -> r2-3 expected on
    # second but got 0. Hmm. Possibly the bar only advances when the
    # sprite actually moves (i.e. not blocked). In E70 the sprite may have
    # been blocked on the second action. But E74 sprite moved and bar
    # didn't advance (bar was at r10-11 already, after=17). 
    #
    # Best consistent rule given E75 (after=18, bar r10-11 -> r12-13? no,
    # E75 shows r10-11 filled, meaning before E75 bar was r8-9, after E75
    # r10-11. So bar advanced 2 rows). And sprite moved left 2 cols.
    # So: bar advances 2 rows per action, sprite moves 2 cols per action.
    # The E70 anomaly (second action 0 changes) is unexplained; mark "?".
    #
    # CLICK on switch cells (3x3 clusters at rows 49-51/54-56/59-61,
    # cols 24-26/29-31/34-36) cycles e->0->2->e. [E67,E72,E73]
    # CLICK elsewhere does nothing. [E17,E31,E33,E49,E57,E61,E68]
    #
    # GOAL (?): unknown. Best guess: arrange the small switch clusters
    # into a target pattern, or move the player sprite to a target column.
    # Predict no level completion (levels stays 0).
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

    def find_sprite(g):
        cells = []
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] == '9':
                    cells.append((r, c))
        if not cells:
            return None
        minc = min(c for _, c in cells)
        maxc = max(c for _, c in cells)
        return (minc, maxc)

    def move_sprite(g, direction):
        changed = {}
        sp = find_sprite(g)
        if sp is None:
            return changed
        lo = 64; hi = -1
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] != '5':
                    if c < lo: lo = c
                    if c > hi: hi = c
        if hi < 0:
            return changed
        width = hi - lo + 1
        new_lo = lo + 2 * direction
        if new_lo < 0 or new_lo + width > 64:
            return changed
        block = [[g[r][c] for c in range(lo, hi + 1)] for r in range(19, 23)]
        for r in range(19, 23):
            for c in range(lo, hi + 1):
                if g[r][c] != '5':
                    g[r][c] = '5'
                    changed[f"{r},{c}"] = '5'
        for i, r in enumerate(range(19, 23)):
            for j in range(width):
                nc = new_lo + j
                if block[i][j] != '5':
                    if g[r][nc] != block[i][j]:
                        g[r][nc] = block[i][j]
                        changed[f"{r},{nc}"] = block[i][j]
        return changed

    def toggle_small_cluster(g, x, y):
        changed = {}
        targets = []
        for rr in (49, 54, 59):
            for cc in (24, 29, 34):
                if cc <= x <= cc + 2 and rr <= y <= rr + 2:
                    targets.append((rr, cc))
        if not targets:
            return changed
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
        return changed

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
            changed.update(move_sprite(grid, +1))
            changed.update(strip_advance(grid, 2))
        elif act in ("ACTION2", "ACTION4"):
            changed.update(move_sprite(grid, -1))
            changed.update(strip_advance(grid, 2))
        elif act.startswith("CLICK"):
            parts = act.split()
            if len(parts) == 3:
                try:
                    x = int(parts[1]); y = int(parts[2])
                except ValueError:
                    x = y = -1
                ch = toggle_small_cluster(grid, x, y)
                if ch:
                    changed.update(ch)
                    changed.update(strip_advance(grid, 2))
        if strip_rows >= 64:
            state = "GAME_OVER"
        steps.append({
            "changes": changed,
            "levels": levels_done,
            "state": state
        })

    return {"steps": steps}
