def predict(probe):
    # Beliefs (with evidence):
    # - Row 63 is a timer bar: '4' = empty, '5' = filled, fills right-to-left [frame: c49-63 are 5, c0-48 are 4]
    # - When the bar becomes fully filled (c0 fills last) state = GAME_OVER [E29, E64]
    # - RESET clears the bar back to empty ('4') and returns NOT_FINISHED [E30, E65, E66, E70]
    # - Most actions advance the bar by one cell [E1,E4,E16,E20,... show r63 cN:5]
    # - CLICK 43 4 / CLICK 37 4 toggle r7 c35-45 between pattern A (c35-39:0,c41-45:3)
    #   and pattern B (c35-39:3,c41-45:0) [E1,E3,E5,E6,E13,E14,E15,E17,E25,E35,E41,E57,E61,E62]
    # - No experiment ever reached levels>=1, so predict no level completion (goal condition "?")
    #   Goal guess "?": likely arranging the central 'f' shapes to a target before the bar fills.

    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)

    # Build mutable grid
    grid = [list(row) for row in frame] if frame else [['5'] * 64 for _ in range(64)]

    def bar_fill(g):
        n = 0
        for c in range(63, -1, -1):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    def clear_bar(g, changes):
        for c in range(64):
            if g[63][c] != '4':
                changes[f"63,{c}"] = '4'
                g[63][c] = '4'

    def toggle_r7(g, changes):
        # detect current pattern at r7 c35-45 and flip
        # pattern A: c35-39 == '0', c41-45 == '3'
        # pattern B: c35-39 == '3', c41-45 == '0'
        seg = [g[7][c] for c in range(35, 46)]
        isA = (seg[0:5] == ['0'] * 5 and seg[6:11] == ['3'] * 5)
        if isA:
            newA = '3'; newB = '0'
        else:
            newA = '0'; newB = '3'
        for c in range(35, 40):
            if g[7][c] != newA:
                changes[f"7,{c}"] = newA
                g[7][c] = newA
        for c in range(41, 46):
            if g[7][c] != newB:
                changes[f"7,{c}"] = newB
                g[7][c] = newB

    steps = []
    state = "NOT_FINISHED"
    levels = level

    for act in actions:
        changes = {}
        act = act.strip()

        if state == "GAME_OVER":
            if act == "RESET":
                clear_bar(grid, changes)
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        if act == "RESET":
            clear_bar(grid, changes)
            state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        # Parse click
        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                x = y = -1
            # r7 toggle on specific clicks
            if (x, y) in ((43, 4), (37, 4)):
                toggle_r7(grid, changes)

        # Advance the timer bar by one cell (best guess: every action advances)
        fill = bar_fill(grid)
        if fill < 64:
            col = 63 - fill
            if grid[63][col] != '5':
                changes[f"63,{col}"] = '5'
                grid[63][col] = '5'
                fill += 1
        if fill >= 64:
            state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
