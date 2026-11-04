import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS (from the evidence)
    #
    # Screen: 64x64, grey (5) playfield. Right strip cols 62-63 is a
    # timer/progress bar that fills with 0 from the top, 2 rows per
    # action that "counts". When it reaches row 63, next action -> GAME_OVER.
    #
    # The "player" is a 4x4 sprite in rows 19-22 (cols vary). It has a
    # 2x2 head (9) on the left and 2x2 tail (a) on the right, with 2s in
    # between. ACTION1/ACTION3 move it RIGHT by 2 columns; ACTION2/ACTION4
    # move it LEFT by 2 columns. [E60,E62,E64,E69,E70,E74: ACTION1 moves
    # sprite right 2 cols; E71: ACTION4 moves left 2 cols]
    #
    # The bar does NOT advance on every action. In E70 (ACTION1,ACTION1
    # from after=6) only the FIRST advanced the bar (r0-1), the second did
    # nothing. In E74 (ACTION1 from after=17) the bar did NOT advance at
    # all but the sprite moved. So the bar advances only when... the
    # sprite is at a particular position? Actually: E74 sprite moved but
    # bar didn't advance; E70 first ACTION1 advanced bar AND moved sprite.
    #
    # Reconsider: the bar advances 2 rows per action, but only up to a
    # cap. In E74 after=17, bar already at rows 0-9 filled (10 rows) from
    # earlier. Hmm, but E70 after=6 bar at r0-1.
    #
    # Simpler reading: the bar advances 2 rows per action UNTIL it is
    # full/capped, and the sprite moves 2 cols per action. E74: bar was
    # already at cap (rows 0-9, 5 bands) so no bar change; sprite moved.
    # E70: bar not capped, first action advanced it, second... also should
    # advance unless capped. E70 second action: 0 changes. So after first
    # ACTION1 bar reached cap (r0-1 -> ... no, that's only 2 rows).
    #
    # Best consistent rule: bar advances 2 rows per action, but the sprite
    # only moves when it can (within bounds). E74 bar didn't move because
    # it was already at its cap for this level (rows 0-9 = 5 bands, 10
    # rows). E70: after=6, bar had r0-1 filled? No—E70 first action filled
    # r0-1, meaning bar was empty before. Second action: 0 changes means
    # bar capped after r0-1?? That contradicts 5 bands.
    #
    # Given uncertainty, model: bar advances 2 rows per action, capped at
    # 10 rows (rows 0-9). Sprite moves 2 cols per action, clamped to
    # playfield. This reproduces E74 (bar capped, sprite moves) and E70
    # partially. Mark cap as "?".
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

    BAR_CAP = 10  # "?" bar fills at most 10 rows (5 bands)

    def strip_advance(g, n=2):
        nonlocal strip_rows
        changed = {}
        for _ in range(n):
            if strip_rows < BAR_CAP and strip_rows < 64:
                r = strip_rows
                for c in (62, 63):
                    if g[r][c] != '0':
                        g[r][c] = '0'
                        changed[f"{r},{c}"] = '0'
                strip_rows += 1
        return changed

    def find_sprite(g):
        # find 9 cells in rows 19-22
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
        # direction +1 = right, -1 = left, by 2 columns
        changed = {}
        sp = find_sprite(g)
        if sp is None:
            return changed
        minc, maxc = sp
        # sprite occupies rows 19-22, cols minc..maxc (head 9 left, tail a right)
        # full sprite width is 4 (2 head + 2 tail) but may be split
        # Determine full sprite extent: rows 19-22, cols minc..(minc+3) typically
        # We'll shift all non-5 cells in rows 19-22 within a window
        # Find window: from minc to maxc, but include 2s between
        # Simplest: shift the contiguous block of non-5 in rows 19-22
        # Find leftmost and rightmost non-5 in rows 19-22
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
        # extract block
        block = [[g[r][c] for c in range(lo, hi + 1)] for r in range(19, 23)]
        # clear old
        for r in range(19, 23):
            for c in range(lo, hi + 1):
                if g[r][c] != '5':
                    g[r][c] = '5'
                    changed[f"{r},{c}"] = '5'
        # place new
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
