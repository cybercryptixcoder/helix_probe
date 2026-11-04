def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a 32-segment budget bar filled with 0 from top,
    #   2 rows per "successful" action [E2,E4,E12,E18].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17].
    # - Clickable objects toggle a 3x3 region among colours e/0/2 [E5,E18,E20].
    #   Cycle order e->0->2->e assumed ("?").
    # - ACTION1/ACTION3 scroll the 2x2 block region left/right [E12,E13,E14] ("?" exact geometry).
    # - ACTION4/ACTION2 permute block colours [E2,E4] ("?").
    # - GOAL: unknown; guess level completes on some switch/block configuration ("?").
    #   No step has yet shown levels>=1, so goal guess is unproven.

    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {"steps": []}

    grid = [list(row) for row in frame]
    ROWS, COLS = len(grid), len(grid[0]) if grid else 0

    # Clickable objects -> their 3x3 toggle regions (row range, col range)
    switch_regions = {
        (30, 50): (49, 51, 29, 31),
        (35, 50): (49, 51, 34, 36),
        (25, 55): (54, 56, 24, 26),
        (30, 55): (54, 56, 29, 31),
        (35, 55): (54, 56, 34, 36),
        (25, 60): (59, 61, 24, 26),
        (30, 60): (59, 61, 29, 31),
        (35, 60): (59, 61, 34, 36),
    }

    def bar_filled_rows(g):
        # count rows where c62 is '0' (filled)
        n = 0
        for r in range(ROWS):
            if COLS >= 63 and g[r][62] == '0':
                n += 1
        return n

    def advance_bar(g, changes):
        filled = bar_filled_rows(g)
        # fill next 2 rows (if available)
        for r in range(filled, min(filled + 2, ROWS)):
            for c in (62, 63):
                if c < COLS and g[r][c] != '0':
                    g[r][c] = '0'
                    changes[f"{r},{c}"] = '0'
        return bar_filled_rows(g)

    def cycle_color(ch):
        # e->0->2->e ("?")
        order = {'e': '0', '0': '2', '2': 'e'}
        return order.get(ch, ch)

    def toggle_switch(g, region, changes):
        r0, r1, c0, c1 = region
        # determine current color (use top-left)
        cur = g[r0][c0]
        new = cycle_color(cur)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if g[r][c] != new:
                    g[r][c] = new
                    changes[f"{r},{c}"] = new

    def shift_block(g, direction, changes):
        # Shift the 2x2 block region (rows 19-22, cols 23-42) left/right by 2 ("?")
        # Approximate: rotate the 4x20 window.
        r0, r1, c0, c1 = 19, 22, 23, 42
        if r1 >= ROWS or c1 >= COLS:
            return
        width = c1 - c0 + 1
        for r in range(r0, r1 + 1):
            row = [g[r][c] for c in range(c0, c1 + 1)]
            if direction < 0:
                row = row[2:] + row[:2]
            else:
                row = row[-2:] + row[:-2]
            for i, c in enumerate(range(c0, c1 + 1)):
                if g[r][c] != row[i]:
                    g[r][c] = row[i]
                    changes[f"{r},{c}"] = row[i]

    steps = []
    state = "NOT_FINISHED"
    levels = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            # only RESET works
            if act == "RESET":
                # reset: refill bar with e, clear switches to e ("?")
                for r in range(ROWS):
                    for c in (62, 63):
                        if c < COLS and grid[r][c] != 'e':
                            grid[r][c] = 'e'
                            changes[f"{r},{c}"] = 'e'
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        if act == "RESET":
            for r in range(ROWS):
                for c in (62, 63):
                    if c < COLS and grid[r][c] != 'e':
                        grid[r][c] = 'e'
                        changes[f"{r},{c}"] = 'e'
            state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        successful = False

        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x, y = int(parts[1]), int(parts[2])
            except Exception:
                x = y = -1
            if (x, y) in switch_regions:
                toggle_switch(grid, switch_regions[(x, y)], changes)
                successful = True
            # else: invalid click, no change, no bar advance

        elif act == "ACTION1":
            shift_block(grid, -1, changes)
            successful = True
        elif act == "ACTION3":
            shift_block(grid, +1, changes)
            successful = True
        elif act in ("ACTION2", "ACTION4"):
            # colour permutation of block ("?")
            r0, r1, c0, c1 = 19, 22, 23, 42
            swap = {'9': 'a', 'a': '9', '2': '2'}
            if r1 < ROWS and c1 < COLS:
                for r in range(r0, r1 + 1):
                    for c in range(c0, c1 + 1):
                        nv = swap.get(grid[r][c], grid[r][c])
                        if grid[r][c] != nv:
                            grid[r][c] = nv
                            changes[f"{r},{c}"] = nv
            successful = True

        if successful:
            filled_before = bar_filled_rows(grid)
            advance_bar(grid, changes)
            filled_after = bar_filled_rows(grid)
            # If bar was already full before this action -> GAME_OVER
            if filled_before >= ROWS:
                state = "GAME_OVER"
            # (goal guess "?": never triggered here)

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
