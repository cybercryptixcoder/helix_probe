def predict(probe):
    # A1: shift lowest non-1 lane block UP 4 rows, preserving pattern [E34,E35]
    #     EXCEPT: if it lands at rows 28-31, it becomes solid 3 [E37 s2] (?)
    # A2: shift lowest non-1 lane block DOWN 4 rows, preserving pattern [E28,E35]
    # A3: move lane LEFT 4 cols [E31,E37]
    # A4: move lane RIGHT 4 cols [E37 s1]
    # A5: toggle lowest UNIFORM 0/3 band in the LANE (0<->3) [E37 s3: solid3->solid0]
    #     non-uniform bands skipped [E24,E26,E28]
    # Counter '4' on row 63 moves LEFT by 1 on some board changes [E1..]; exact trigger
    #   uncertain (?): observed moving on A1 [E37 s2] but not on A4 [E37 s1] or A5 [E37 s3].
    #   Keep: moves on A1/A2 vertical shifts that change board.
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
        counter_moves = False

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
                    # ? if landing at top band rows 28-31, fill solid 3 [E37 s2]
                    if nr0 == 28:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][c0+j] = "3"
                    else:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][c0+j] = band[k][j]
                    changed = True
                    counter_moves = True
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
            for r0 in range(56, -1, -4):
                vals = [grid[r0+k][c0+j] for k in range(4) for j in range(4)]
                if all(v == "0" for v in vals):
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][c0+j] = "3"
                    changed = True
                    break
                elif all(v == "3" for v in vals):
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][c0+j] = "0"
                    changed = True
                    break

        if counter_col is not None and counter_col > 0 and counter_moves:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
