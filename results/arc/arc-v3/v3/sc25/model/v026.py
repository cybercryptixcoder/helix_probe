def predict(probe):
    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {"steps": []}
    grid = [list(row) for row in frame]
    ROWS = len(grid)
    COLS = len(grid[0]) if grid else 0

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

    def bar_filled(g):
        n = 0
        for r in range(ROWS):
            if COLS >= 63 and g[r][62] == '0':
                n += 1
        return n

    def advance_bar(g, changes):
        filled = bar_filled(g)
        for r in range(filled, min(filled + 2, ROWS)):
            for c in (62, 63):
                if c < COLS and g[r][c] != '0':
                    g[r][c] = '0'
                    changes[f"{r},{c}"] = '0'

    def cycle_color(ch):
        order = {'e': '0', '0': '2', '2': 'e'}
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
        for r in range(19, 23):
            for c in range(23, 43):
                if g[r][c] in ('9', 'a'):
                    return (r, c)
        return None

    def shift_player(g, direction, changes):
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        nc0 = c0 + direction * 4
        if nc0 < 23 or nc0 + 3 > 42:
            return
        for r in range(r0, r0 + 4):
            for c in range(c0, c0 + 4):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
        for r in range(r0, r0 + 4):
            for c in (nc0, nc0 + 1):
                if g[r][c] != '9':
                    g[r][c] = '9'
                    changes[f"{r},{c}"] = '9'
            for c in (nc0 + 2, nc0 + 3):
                if g[r][c] != 'a':
                    g[r][c] = 'a'
                    changes[f"{r},{c}"] = 'a'

    def toggle_player(g, changes):
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        for r in range(r0, r0 + 4):
            for c in range(c0, c0 + 4):
                ch = g[r][c]
                if ch == '9':
                    g[r][c] = 'a'; changes[f"{r},{c}"] = 'a'
                elif ch == 'a':
                    g[r][c] = '9'; changes[f"{r},{c}"] = '9'

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
                            grid[r][c] = 'e'; changes[f"{r},{c}"] = 'e'
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        if act == "RESET":
            for r in range(ROWS):
                for c in (62, 63):
                    if c < COLS and grid[r][c] != 'e':
                        grid[r][c] = 'e'; changes[f"{r},{c}"] = 'e'
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
            # E50,E52,E58,E60,E62: no sprite move, bar only
            successful = True
        elif act == "ACTION3":
            shift_player(grid, -1, changes)
            successful = True
        elif act == "ACTION2":
            toggle_player(grid, changes)
            successful = True
        elif act == "ACTION4":
            shift_player(grid, +1, changes)
            toggle_player(grid, changes)
            successful = True

        if successful:
            filled_before = bar_filled(grid)
            advance_bar(grid, changes)
            if filled_before >= ROWS:
                state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
