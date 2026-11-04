import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS (revised v31)
    #
    # Screen: 64x64 grey (5) playfield. Right strip cols 62-63 is a
    # timer/progress bar that fills with 0 from the top, 2 rows per
    # action that "counts". When it reaches row 64, next action -> GAME_OVER.
    #
    # The "player" is a 4x4 sprite in rows 19-22: 2x2 head (9) on left,
    # 2x2 tail (a) on right, 2s between. It moves horizontally by 2 cols
    # per ACTION1(->right)/ACTION2(->left). ACTION3/ACTION4 mirror.
    # [E60,E62,E64,E69,E70,E74: ACTION1 moves sprite right 2 cols]
    # [E71,E75: ACTION4 moves left 2 cols]
    #
    # KEY: the sprite is BLOCKED at the right edge (c41-42). When blocked,
    # ACTION1 does NOTHING at all — no sprite move AND no bar advance.
    # [E82: ACTION1 at right edge -> 0 changes]
    # [E84: ACTION1 -> bar advanced (sprite moved to edge), then ACTION1
    #        -> 0 changes (blocked)]
    # [E86: ACTION1 -> 0 changes (blocked, sprite at edge), then ACTION1
    #        -> bar advanced (sprite moved off edge), then ACTION1 -> bar]
    # So: when the sprite is at the right edge, ACTION1 is a no-op
    # (no bar). Otherwise ACTION1 moves sprite right 2 AND advances bar 2.
    # Symmetric guess: ACTION2 blocked at left edge -> no-op.
    #
    # CLICK on switch cells (3x3 clusters at rows 49-51/54-56/59-61,
    # cols 24-26/29-31/34-36) cycles e->0->2->e. [E67,E72,E73,E78,E79]
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

    def sprite_span(g):
        # Find the horizontal span of the 4x4 sprite in rows 19-22.
        # The sprite is the contiguous block of non-5 cells in rows 19-22.
        lo = 64; hi = -1
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] != '5':
                    if c < lo: lo = c
                    if c > hi: hi = c
        return lo, hi

    def move_sprite(g, direction):
        # Move the 4x4 sprite block (rows 19-22) horizontally by 2 cols.
        # Returns (changed, moved_bool).
        changed = {}
        lo, hi = sprite_span(g)
        if hi < 0:
            return changed, False
        width = hi - lo + 1
        new_lo = lo + 2 * direction
        if new_lo < 0 or new_lo + width > 64:
            return changed, False
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
        return changed, True

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
            ch, moved = move_sprite(grid, +1)
            if moved:
                changed.update(ch)
                changed.update(strip_advance(grid, 2))
            # if blocked: no-op (no bar advance)
        elif act in ("ACTION2", "ACTION4"):
            ch, moved = move_sprite(grid, -1)
            if moved:
                changed.update(ch)
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
