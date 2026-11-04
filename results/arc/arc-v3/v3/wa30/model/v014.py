def predict(probe):
    # Beliefs (revised after E52):
    # - The screen has static obstacle blocks (4/9 and 9/2 patterns) plus ONE movable
    #   4x4 "player" block containing 0/e cells. [E1-E52]
    # - A1/A2 move the player up/down by 4 rows; A3/A4 move it left/right by 4 cols;
    #   a move is blocked if the target 4x4 region is not empty (all '1'). [E1-E52]
    # - A5 toggles the lowest uniform-0/3 block in the player's column (0<->3). [E24,E32,E44]
    # - Row-63 counter '4' moves left by 1 on SOME actions; exact rule uncertain. [E48,E50,E51,E52]
    #   ? best guess: counter moves on a successful player move that changes column,
    #     and on A5 when a toggle occurs. (E50/E51 remain unexplained.)
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

    def find_player():
        # find 4x4 aligned region (rows 0..59, cols 0..60) with most 0/e cells
        best = None; bestn = -1
        for r0 in range(0, 60, 4):
            for c0 in range(0, 61, 4):
                n = 0
                for k in range(4):
                    for j in range(4):
                        v = grid[r0+k][c0+j]
                        if v in ("0", "e"):
                            n += 1
                if n > bestn:
                    bestn = n; best = (r0, c0)
        return best

    def region_empty(r0, c0):
        if r0 < 0 or r0 > 59 or c0 < 0 or c0 > 60:
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
        counter_moves = False

        if a in ("ACTION1", "ACTION2", "ACTION3", "ACTION4"):
            pl = find_player()
            if pl is not None:
                r0, c0 = pl
                if a == "ACTION1":
                    nr0, nc0 = r0 - 4, c0
                elif a == "ACTION2":
                    nr0, nc0 = r0 + 4, c0
                elif a == "ACTION3":
                    nr0, nc0 = r0, c0 - 4
                else:
                    nr0, nc0 = r0, c0 + 4
                if 0 <= nr0 <= 59 and 0 <= nc0 <= 60 and region_empty(nr0, nc0):
                    band = [[grid[r0+k][c0+j] for j in range(4)] for k in range(4)]
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][c0+j] = "1"
                    # ? landing at rows 28-31 becomes solid 3 (old belief)
                    if nr0 == 28:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][nc0+j] = "3"
                    else:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][nc0+j] = band[k][j]
                    # ? counter moves on horizontal moves (best guess)
                    if a in ("ACTION3", "ACTION4"):
                        counter_moves = True
        elif a == "ACTION5":
            pl = find_player()
            if pl is not None:
                c0 = pl[1]
                for r0 in range(56, -1, -4):
                    vals = [grid[r0+k][c0+j] for k in range(4) for j in range(4)]
                    if all(v == "0" for v in vals):
                        for k in range(4):
                            for j in range(4):
                                grid[r0+k][c0+j] = "3"
                        counter_moves = True
                        break
                    elif all(v == "3" for v in vals):
                        for k in range(4):
                            for j in range(4):
                                grid[r0+k][c0+j] = "0"
                        counter_moves = True
                        break

        if counter_col is not None and counter_col > 0 and counter_moves:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
