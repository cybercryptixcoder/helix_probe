def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget bar filled with 0 from top, 2 rows per
    #   "successful" action [E2,E4,E12,E18,E22,E23,E24,E25,E26].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25].
    # - Clickable objects toggle a 3x3 region among colours e/0/2 [E5,E18,E20,E22,E23].
    #   Cycle order e->2->0->e (observed: e then 2 then e then 2... on repeat clicks) [E22,E23].
    # - ACTION1/ACTION3 shift the player 2x2 block left/right by 2 cols; only the
    #   player's own cells change (8 cells), not the whole window [E13,E14,E24].
    # - ACTION2/ACTION4 toggle the player's 9/a colours (no horizontal shift) [E25,E26].
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
        n = 0
        for r in range(ROWS):
            if COLS >= 63 and g[r][62] == '0':
                n += 1
        return n

    def advance_bar(g, changes):
        filled = bar_filled_rows(g)
        for r in range(filled, min(filled + 2, ROWS)):
            for c in (62, 63):
                if c < COLS and g[r][c] != '0':
                    g[r][c] = '0'
                    changes[f"{r},{c}"] = '0'

    def cycle_color(ch):
        # e->2->0->e (observed on repeated clicks) [E22,E23]
        order = {'e': '2', '2': '0', '0': 'e'}
        return order.get(ch, ch)

    def toggle_switch(g, region, changes):
        r0, r1, c0, c1 = region
        cur = g[r0][c0]
        new = cycle_color(cur)
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                if g[r][c] != new:
                    g[r][c] = new
                    changes[f"{r},{c}"] = new

    def find_player(g):
        # locate the 2x2 9/a block in rows 19-22 region; return (r0,c0) top-left
        # player occupies rows 19-22, cols 23-42; find leftmost 9/a cell
        for r in range(19, 23):
            for c in range(23, 43):
                if g[r][c] in ('9', 'a'):
                    # top-left of the 2x2 block: rows r..r+1, cols c..c+1
                    return (r, c)
        return None

    def shift_player(g, direction, changes):
        # shift the 2x2 player block left/right by 2 cols within cols 23-42
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        c1 = c0 + 1
        nc0 = c0 + direction * 2
        if nc0 < 23 or nc0 + 1 > 42:
            return  # blocked at edge
        # clear old cells
        for r in (r0, r0 + 1):
            for c in (c0, c1):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
        # write new cells preserving colours (top row 9, bottom row a)
        top = '9'
        bot = 'a'
        for r, col in ((r0, top), (r0 + 1, bot)):
            for c in (nc0, nc0 + 1):
                if g[r][c] != col:
                    g[r][c] = col
                    changes[f"{r},{c}"] = col

    def toggle_player_colors(g, changes):
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        for r in (r0, r0 + 1):
            for c in (c0, c0 + 1):
                ch = g[r][c]
                if ch == '9':
                    g[r][c] = 'a'
                    changes[f"{r},{c}"] = 'a'
                elif ch == 'a':
                    g[r][c] = '9'
                    changes[f"{r},{c}"] = '9'

    steps = []
    state = "NOT_FINISHED"
    levels = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
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

        elif act == "ACTION1":
            shift_player(grid, -1, changes)
            successful = True
        elif act == "ACTION3":
            shift_player(grid, +1, changes)
            successful = True
        elif act in ("ACTION2", "ACTION4"):
            toggle_player_colors(grid, changes)
            successful = True

        if successful:
            filled_before = bar_filled_rows(grid)
            advance_bar(grid, changes)
            if filled_before >= ROWS:
                state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
