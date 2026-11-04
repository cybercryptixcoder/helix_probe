import copy

def predict(probe):
    # ------------------------------------------------------------------
    # BELIEFS (from the evidence)
    #
    # The screen is 64x64. There is a big grey (5) playfield, a right-hand
    # column strip (cols 62-63) that is a "progress / timer" bar, and a
    # set of small coloured puzzle cells around rows 19-22 (the "row of
    # blocks") plus other block clusters.
    #
    # ACTION1: advances a "cursor" one step and shifts/cycles the block
    #   cluster in rows 19-22 one position left, and advances the right
    #   strip by 2 rows. [E2,E4,E12,E13,E24,E28,E50,E58,E64,E69,E70]
    # ACTION2: shifts the block cluster one position right (opposite of
    #   ACTION1) and advances the strip by 2 rows. [E4,E25,E26,E40,E48,
    #   E54,E55,E56]
    # ACTION3: shifts the block cluster one position left (like ACTION1
    #   but without the strip advance sometimes) and advances strip.
    #   [E2,E6,E12,E27,E28,E30,E32,E34,E37,E38,E44,E53,E65]
    # ACTION4: shifts the block cluster one position right, advances
    #   strip. [E2,E4,E7,E11,E19,E39,E42,E71]
    # CLICK x y: clicking certain "button" cells toggles a small block
    #   cluster (rows 49-51 or 54-56 or 59-61, cols 24-36) between
    #   e/0/2 and advances the strip by 2 rows. [E1,E3,E5,E6,E7,E8,E9,
    #   E18,E19,E20,E21,E22,E23,E25,E29,E35,E41,E43,E45,E51,E53,E55,
    #   E59,E63,E65]
    #   Clicking non-button cells does nothing. [E17,E31,E33,E49,E57,
    #   E61,E67,E68,E69,E71]
    #
    # The right strip (cols 62-63) fills with 0 from the top, 2 rows per
    # action that "counts". When it reaches the bottom (row 63) the next
    # counting action causes GAME_OVER. [E14,E15,E34,E35,E60,E62]
    # RESET restores the level to its starting state.
    #
    # GOAL (?): level 1 is completed when the block cluster in rows 19-22
    # is arranged into the target pattern (all 2s in a contiguous run?).
    # Best guess: the strip reaching full is bad; the goal is to make the
    # row-19-22 cluster match a target. Since no experiment ever completed
    # it, mark goal as "?" and predict no level completion.
    # ------------------------------------------------------------------

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    # Build mutable grid from frame (list of strings -> list of lists)
    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    # Replay history to reconstruct internal state that isn't visible:
    # mainly the strip fill height (rows of cols 62-63 filled with 0)
    # and the block cluster offset. We derive from the grid directly
    # where possible, but track a counter for strip.
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
        # fill next n rows of cols 62-63 with 0, from current top
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

    def shift_cluster(g, direction):
        # shift the row 19-22 block cluster (cols ~23-42) one step.
        # direction -1 = left, +1 = right.
        # We model it as: the pattern of 9/a/2 in rows 19-22 shifts.
        changed = {}
        # Extract rows 19-22, cols 23-42
        r0, r1 = 19, 22
        c0, c1 = 23, 42
        block = [[g[r][c] for c in range(c0, c1 + 1)] for r in range(r0, r1 + 1)]
        # shift
        newblock = []
        for row in block:
            if direction < 0:
                newrow = row[1:] + [row[0]]
            else:
                newrow = [row[-1]] + row[:-1]
            newblock.append(newrow)
        for i, r in enumerate(range(r0, r1 + 1)):
            for j, c in enumerate(range(c0, c1 + 1)):
                if g[r][c] != newblock[i][j]:
                    g[r][c] = newblock[i][j]
                    changed[f"{r},{c}"] = newblock[i][j]
        return changed

    def toggle_small_cluster(g, x, y):
        # button cells: clicking toggles the 3x3 cluster at rows 49-51,
        # 54-56, or 59-61, cols 24-26, 29-31, 34-36
        changed = {}
        # determine which cluster
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
            # restore to level start (unknown exact); we approximate by
            # resetting strip and clusters to a neutral state.
            # We don't have the true start frame, so just clear strip.
            for r in range(64):
                for c in (62, 63):
                    if grid[r][c] != 'e':
                        grid[r][c] = 'e'
                        changed[f"{r},{c}"] = 'e'
            strip_rows = 0
            state = "NOT_FINISHED"
        elif act == "ACTION1":
            changed.update(shift_cluster(grid, -1))
            changed.update(strip_advance(grid, 2))
        elif act == "ACTION2":
            changed.update(shift_cluster(grid, +1))
            changed.update(strip_advance(grid, 2))
        elif act == "ACTION3":
            changed.update(shift_cluster(grid, -1))
            changed.update(strip_advance(grid, 2))
        elif act == "ACTION4":
            changed.update(shift_cluster(grid, +1))
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
        # check game over: strip full
        if strip_rows >= 64:
            state = "GAME_OVER"
        steps.append({
            "changes": changed,
            "levels": levels_done,
            "state": state
        })

    return {"steps": steps}
