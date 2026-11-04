def predict(probe):
    # Beliefs (revised after E39):
    # - The "lane" is a 4-wide column of 4x4 blocks that moves L/R by 4 (A3/A4) and
    #   whose blocks shift up/down by 4 (A1/A2). [E1..E39]
    # - A3/A4 move the lane by copying the lane's column contents into the new
    #   column and clearing the old column. [E6, E29, E31, E37, E39]
    # - A1/A2 shift the LOWEST non-empty block of the lane by 4 rows; the block
    #   keeps its pattern EXCEPT when it lands at rows 28-31, where it becomes
    #   solid 3. [E37, E38]
    # - A5 toggles the lowest UNIFORM 0/3 block in the lane (0<->3); non-uniform
    #   blocks are skipped. [E24, E26, E28, E32, E37, E38]
    # - The counter '4' on row 63 moves LEFT by 1 on some board changes.
    #   Observed moving on: A1 (E37, E38), A2 (E27, E28, E35, E39), A5 (E26, E33,
    #   E35, E36, E38). Not on A3/A4 alone (E37 s1, E39 s1/s4).
    #   ? Best guess: counter moves on A1, A2, and A5 (i.e. any action that
    #   changes the lane's vertical structure or toggles a block), but NOT on
    #   pure horizontal A3/A4 moves. E39 s3 (A2) moved it; E39 s1 (A3) did not;
    #   E39 s4 (A3) did not. E37 s1 (A4) did not. E37 s2 (A1) did.
    #   E38 s2 (A5) did. E33 (A5) did. E34 s2 (A5) did NOT (no uniform block).
    #   So refine: A5 moves counter only when it actually toggles a block.
    #   A1/A2 move counter only when they actually shift a block.
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
                    if nr0 == 28:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][c0+j] = "3"
                    else:
                        for k in range(4):
                            for j in range(4):
                                grid[nr0+k][c0+j] = band[k][j]
                    counter_moves = True
        elif a in ("ACTION3", "ACTION4"):
            dc = -4 if a == "ACTION3" else 4
            nc0 = c0 + dc
            if 0 <= nc0 <= 60:
                for r in range(63):
                    for j in range(4):
                        grid[r][nc0+j] = grid[r][c0+j]
                        grid[r][c0+j] = "1"
        elif a == "ACTION5":
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
