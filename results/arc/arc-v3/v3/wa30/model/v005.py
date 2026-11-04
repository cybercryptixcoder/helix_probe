def predict(probe):
    # Lane A = cols 32-35, lane B = cols 36-39. Blocks 4 rows tall.
    # ACTION1: shift lane-A blocks UP by 4 rows [E2, E4, E7, E8]
    # ACTION2: shift lane-A blocks DOWN by 4 rows [E4, E7, E8]
    # ACTION3: move lane-A stack into lane B (clearing lane A) [E6]
    # ACTION4: move lane-B stack into lane A (clearing lane B) [E6]
    # ACTION5: recolour a lane-A block (3-colour) [E7 step3] ?
    # Counter: single '4' on row 63 moves LEFT by 1 on some actions [E4,E6,E7,E8]
    #   ? moves when a shift/move actually changes the board
    # ? Goal: unknown; guess counter reaching col 0, or lane A == lane B.
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
        moved = False

        if a == "ACTION1":
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r + 4
                    grid[r][c] = col[src] if src < 64 else "1"
            moved = True
        elif a == "ACTION2":
            for c in range(32, 36):
                col = [grid[r][c] for r in range(64)]
                for r in range(64):
                    src = r - 4
                    grid[r][c] = col[src] if src >= 0 else "1"
            moved = True
        elif a == "ACTION3":
            # move lane A stack to lane B
            for r in range(64):
                for k in range(4):
                    grid[r][36 + k] = grid[r][32 + k]
                    grid[r][32 + k] = "1"
            moved = True
        elif a == "ACTION4":
            for r in range(64):
                for k in range(4):
                    grid[r][32 + k] = grid[r][36 + k]
                    grid[r][36 + k] = "1"
            moved = True
        elif a == "ACTION5":
            # ? recolour: turn a lane-A 0/e block into 3-block
            for r0 in range(60, -1, -4):
                vals = [grid[r0 + k][32] for k in range(4)]
                if any(v in ("0", "e") for v in vals):
                    for k in range(4):
                        for c in range(32, 36):
                            grid[r0 + k][c] = "3"
                    moved = True
                    break

        if counter_col is not None and counter_col > 0 and moved:
            grid[63][counter_col] = "7"
            counter_col -= 1
            grid[63][counter_col] = "4"

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
