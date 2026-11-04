def predict(probe):
    # Mechanism (from the notebook evidence):
    # The world has two vertical "lanes" of 4-wide blocks: lane A = cols 32-35,
    # lane B = cols 36-39. Blocks are 4 rows tall. The screen is 64x64.
    #
    # ACTION1: shifts the whole lane-A stack UP by 4 rows (a block moves from
    #   r40-43 to r36-39, etc.) [E2, E4]. Top block leaves at top.
    # ACTION2: shifts the lane-A stack DOWN by 4 rows [E4: r40-43 -> r44-47;
    #   E5: r41-42 content moved down]. Bottom block leaves at bottom.
    # ACTION3: moves a block from lane A (cols 32-35) into lane B (cols 36-39)
    #   at the same rows [E1 step3, E3 step2/4].
    # ACTION4: moves a block from lane B into lane A at same rows [E1 step1,
    #   E3 step1/3].
    # ACTION5: does nothing to the world; it only advances the bottom-row
    #   counter [E1 step4 no change, E4 step2 only r63 c60:4].
    #
    # The bottom row r63 is a counter: a single '4' marker that moves LEFT by
    # one column per action (any action) [E1 c63->c62->c61, E2 c62, E3 c61,
    # E4 c60, ...]. Everything else in r63 is '7'.
    #
    # We cannot fully simulate the block stacks without tracking the whole
    # world state, which the probe's "frame" gives us. We use the frame to
    # locate the counter and to move blocks by the rules above.
    #
    # ? Goal: unknown. Best guess: the counter reaching column 0, or a block
    # arrangement. We do NOT predict level completion (levels stays 0).

    actions = probe.get("actions", [])
    frame = probe.get("frame", None)

    # Build a mutable grid from the frame if available.
    grid = None
    if frame is not None:
        try:
            grid = [list(row) for row in frame]
        except Exception:
            grid = None

    def get(r, c):
        return grid[r][c]

    def setc(r, c, v):
        grid[r][c] = v

    def snapshot_changes(before):
        ch = {}
        for r in range(64):
            for c in range(64):
                if grid[r][c] != before[r][c]:
                    ch["%d,%d" % (r, c)] = grid[r][c]
        return ch

    # Counter position: rightmost '4' in row 63.
    counter_col = None
    if grid is not None:
        row63 = "".join(grid[63])
        pos = row63.rfind("4")
        if pos >= 0:
            counter_col = pos

    steps = []
    for a in actions:
        if grid is None:
            steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
            continue

        before = [row[:] for row in grid]

        # --- world block motions ---
        if a == "ACTION1":
            # Shift lane A (cols 32-35) up by 4 rows.
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r + 4
                    grid[r][c] = col[src] if src < 64 else "1"
        elif a == "ACTION2":
            # Shift lane A (cols 32-35) down by 4 rows.
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r - 4
                    grid[r][c] = col[src] if src >= 0 else "1"
        elif a == "ACTION3":
            # Move a lane-A block into lane B at same rows.
            # Find the lowest non-1 block in lane A and copy to lane B.
            for r0 in range(60, -1, -4):
                block = [grid[r0 + k][32] for k in range(4)]
                if any(v != "1" for v in block):
                    for k in range(4):
                        for c in range(32, 36):
                            grid[r0 + k][c] = "1"
                        for c in range(36, 40):
                            grid[r0 + k][c] = block[k]
                    break
        elif a == "ACTION4":
            # Move a lane-B block into lane A at same rows.
            for r0 in range(60, -1, -4):
                block = [grid[r0 + k][36] for k in range(4)]
                if any(v != "1" for v in block):
                    for k in range(4):
                        for c in range(36, 40):
                            grid[r0 + k][c] = "1"
                        for c in range(32, 36):
                            grid[r0 + k][c] = block[k]
                    break
        # ACTION5: no world change.

        # --- counter moves left by 1 for every action ---
        if counter_col is not None and counter_col > 0:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snapshot_changes(before),
                      "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
