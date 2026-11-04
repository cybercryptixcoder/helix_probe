def predict(probe):
    # Lane = 4-wide column band holding the block stack; it MOVES horizontally.
    # ACTION1: shift all blocks in lane UP by 4 rows [E13 s2, E11 s2, E2]
    # ACTION2: shift all blocks in lane DOWN by 4 rows [E4 s1, E8 s1]
    # ACTION3: move lane LEFT by 4 cols (blocks copied, old cols -> 1) [E13 s3, E1 s3, E11 s3]
    # ACTION4: move lane RIGHT by 4 cols [E1 s1, E13 s4]
    # ACTION5: acts on FIXED cols 32-35 (not the lane): find lowest 4-row block that is
    #   UNIFORMLY 0 or UNIFORMLY 3, toggle it (0<->3). Non-uniform blocks are skipped.
    #   [E14 s1: 3-block at 32-35 ->0 while lane at 28-31; E14 s2: 0->3; E5: 3->0;
    #    E7 s3: 0->3; E9 s1/E10 s1/E12 s1/E13 s1: non-uniform block -> no change]
    # ACTION5 does NOT advance the counter [E5, E7, E14 s1, E14 s2].
    # Counter '4' on row 63 moves LEFT by 1 when a lane move/shift changes board
    #   [E1,E4,E6,E7,E8,E9,E10,E11,E12,E13,E14 s3].
    # ? Goal: unknown; guess counter reaching col 0 or a target arrangement.
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

    def lane_blocks(c0):
        blocks = []
        for r0 in range(0, 60, 4):
            vals = [grid[r0+k][c0+j] for k in range(4) for j in range(4)]
            if any(v != "1" for v in vals):
                blocks.append(r0)
        return blocks

    counter_col = None
    if grid is not None:
        pos = "".join(grid[63]).rfind("4")
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
            blocks = lane_blocks(c0)
            if blocks:
                lane = [[grid[r][c0+j] for j in range(4)] for r in range(63)]
                newlane = [["1"]*4 for _ in range(63)]
                dy = -4 if a == "ACTION1" else 4
                for r0 in blocks:
                    for k in range(4):
                        nr = r0 + dy + k
                        if 0 <= nr < 63:
                            for j in range(4):
                                newlane[nr][j] = lane[r0+k][j]
                for r in range(63):
                    for j in range(4):
                        if grid[r][c0+j] != newlane[r][j]:
                            changed = True
                        grid[r][c0+j] = newlane[r][j]
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
            # fixed cols 32-35; lowest uniform-0 or uniform-3 block; toggle
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
            # ACTION5 does not advance counter

        if a != "ACTION5" and counter_col is not None and counter_col > 0 and changed:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
