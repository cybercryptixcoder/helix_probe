def predict(probe):
    # A1: shift the LOWEST non-1 block in the lane UP by 4 rows [E19: r44-47->r40-43;
    #     E21: r40-43->r36-39; the 9/2 block at r28-31 never moves]. "?" lowest-block guess.
    # A2: shift the LOWEST non-1 block in the lane DOWN by 4 rows [E4 s1, E8 s1]
    # A3: move lane LEFT by 4 cols (copy, old cols -> 1) [E13 s3, E1 s3, E11 s3]
    # A4: move lane RIGHT by 4 cols [E1 s1, E13 s4]
    # A5: acts on FIXED cols 32-35: find lowest 4-row block that is UNIFORMLY 0 or 3,
    #     toggle it (0<->3). Non-uniform blocks skipped. [E14 s1,s2; E5; E7 s3; E16; E18; E20]
    # Counter '4' on row 63 is the LEFTMOST '4' (7s fill to its left; trailing 4s are
    #   unused counter slots). Moves LEFT by 1 whenever a lane move/shift/toggle changes
    #   the board [E1,E4,E6-E14,E16,E18,E19,E20,E21].
    # ? Goal: unknown; guess counter reaching col 0.
    actions = probe.get("actions", [])
    frame = probe.get("frame", None)
    grid = None
    if frame is not None:
        try:
            grid = [list(row) for row in frame]
        except Exception:
            grid = None

    def snap(before):
        ch = {}
        for r in range(64):
            for c in range(64):
                if grid[r][c] != before[r][c]:
                    ch["%d,%d" % (r, c)] = grid[r][c]
        return ch

    def find_lane():
        best = None; bestn = -1
        for c0 in range(0, 64, 4):
            n = 0
            for r in range(63):
                for c in range(c0, c0+4):
                    if grid[r][c] != "1":
                        n += 1
            if n > bestn:
                bestn = n; best = c0
        return best if best is not None else 32

    def lowest_block(c0):
        # bottom-up: first 4-row band (aligned to 4) that is not all 1s
        for r0 in range(56, -1, -4):
            vals = [grid[r0+k][c0+j] for k in range(4) for j in range(4)]
            if any(v != "1" for v in vals):
                return r0
        return None

    def band_empty(r0, c0):
        if r0 < 0 or r0 > 59:
            return False
        for k in range(4):
            for j in range(4):
                if grid[r0+k][c0+j] != "1":
                    return False
        return True

    counter_col = None
    if grid is not None:
        pos = "".join(grid[63]).find("4")
        if pos >= 0:
            counter_col = pos

    steps = []
    for a in actions:
        if grid is None:
            steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
            continue
        before = [row[:] for row in grid]
        c0 = find_lane()
        changed = False

        if a in ("ACTION1", "ACTION2"):
            r0 = lowest_block(c0)
            if r0 is not None:
                dy = -4 if a == "ACTION1" else 4
                nr0 = r0 + dy
                if 0 <= nr0 <= 59 and band_empty(nr0, c0):
                    band = [[grid[r0+k][c0+j] for j in range(4)] for k in range(4)]
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][c0+j] = "1"
                    for k in range(4):
                        for j in range(4):
                            grid[nr0+k][c0+j] = band[k][j]
                    changed = True
        elif a in ("ACTION3", "ACTION4"):
            dc = -4 if a == "ACTION3" else 4
            nc0 = c0 + dc
            if 0 <= nc0 <= 60:
                for r in range(63):
                    for j in range(4):
                        grid[r][nc0+j] = grid[r][c0+j]
                        grid[r][c0+j] = "1"
                changed = True
        elif a == "ACTION5":
            fc = 32
            for r0 in range(56, -1, -4):
                vals = [grid[r0+k][fc+j] for k in range(4) for j in range(4)]
                if all(v == "0" for v in vals):
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][fc+j] = "3"
                    changed = True
                    break
                elif all(v == "3" for v in vals):
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][fc+j] = "0"
                    changed = True
                    break

        if counter_col is not None and counter_col > 0 and changed:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
