def predict(probe):
    # Mechanism (from the notebook evidence):
    # The world has two vertical "lanes" of 4-wide blocks: lane A = cols 32-35,
    # lane B = cols 36-39. Blocks are 4 rows tall. The screen is 64x64.
    #
    # ACTION1: shifts the whole lane-A stack UP by 4 rows [E2, E4].
    # ACTION2: shifts the whole lane-A stack DOWN by 4 rows [E4, E5].
    # ACTION3: moves a lane-A block into lane B at same rows [E1, E3, E6].
    # ACTION4: moves a lane-B block into lane A at same rows [E1, E3, E6].
    # ACTION5: does nothing to the world; only advances the bottom-row counter
    #   [E1 step4 no change, E4 step2 only r63 c60:4].
    #
    # The bottom row r63 is a counter: a single '4' marker that moves LEFT by
    # one column per action (any action) [E1 c63->c62->c61, E2 c62, E3 c61,
    # E4 c60, E5 c59, E6 c59->c58].
    #
    # ? Goal: unknown. Best guess: the counter reaching column 0, or a block
    # arrangement. We do NOT predict level completion (levels stays 0).

    actions = probe.get("actions", [])
    frame = probe.get("frame", None)

    grid = None
    if frame is not None:
        try:
            grid = [list(row) for row in frame]
        except Exception:
            grid = None

    def snapshot_changes(before):
        ch = {}
        for r in range(64):
            for c in range(64):
                if grid[r][c] != before[r][c]:
                    ch["%d,%d" % (r, c)] = grid[r][c]
        return ch

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

        if a == "ACTION1":
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r + 4
                    grid[r][c] = col[src] if src < 64 else "1"
        elif a == "ACTION2":
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r - 4
                    grid[r][c] = col[src] if src >= 0 else "1"
        elif a == "ACTION3":
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
            for r0 in range(60, -1, -4):
                block = [grid[r0 + k][36] for k in range(4)]
                if any(v != "1" for v in block):
                    for k in range(4):
                        for c in range(36, 40):
                            grid[r0 + k][c] = "1"
                        for c in range(32, 36):
                            grid[r0 + k][c] = block[k]
                    break

        if counter_col is not None and counter_col > 0:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snapshot_changes(before),
                      "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
