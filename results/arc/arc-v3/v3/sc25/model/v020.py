def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   successful action [E2,E4,E12,E18,E22,E23,E24,E25,E26,E37,E38].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15,E35].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29].
    # - Clickable 3x3 blocks toggle colour among e/0/2 [E5,E18,E20,E22,E23].
    #   Cycle order e->2->0->e (observed on repeated clicks) [E22,E23].
    # - ACTION1/ACTION3 move the player LEFT/RIGHT by 2 cols per press [E24,E27,E28,E30,E32,E34,E38].
    #   The player is a 2x2 "head" (top row 9, bottom row a) with a 2x2 "tail" (top a, bottom 9)
    #   immediately to its right, and a 2x2 "2" trail behind the tail [E27,E28,E38].
    #   Actually the player is a 4-wide, 4-tall sprite: cols c..c+1 = head (9/a), c+2..c+3 = tail (a/9).
    #   Moving shifts the whole 4-wide sprite by 2 cols; vacated cells become 2 [E27,E28,E38].
    #   Wait: observed r19 c31-32:9, c33-34:a, c35-38:2 after moving left to c31.
    #   So head at c31-32 (9 top, a bottom), tail at c33-34 (a top, 9 bottom), trail 2 at c35-38.
    #   Initial head at c39-40, tail at c41-42 [E36].
    # - ACTION2/ACTION4 toggle the player's 9/a colours in place (no shift) [E25,E26].
    # - GOAL: unknown; guess level completes when the player reaches a target ("?").

    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {"steps": []}

    grid = [list(row) for row in frame]
    ROWS, COLS = len(grid), len(grid[0]) if grid else 0

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
        # locate the 2x2 9/a head block in rows 19-22, cols 23-42
        for r in range(19, 23):
            for c in range(23, 43):
                if g[r][c] in ('9', 'a'):
                    return (r, c)
        return None

    def shift_player(g, direction, changes):
        # Move the 4-wide player sprite (head 2 cols + tail 2 cols) left/right by 2 cols.
        # Head: top row 9, bottom row a. Tail: top row a, bottom row 9.
        # Vacated cells become 2.
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        nc0 = c0 + direction * 2
        if nc0 < 23 or nc0 + 3 > 42:
            return
        # clear old sprite cells (head + tail) to 2
        for r in (r0, r0 + 1):
            for c in range(c0, c0 + 4):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
        # write new sprite: head at nc0..nc0+1, tail at nc0+2..nc0+3
        for r, head_col, tail_col in ((r0, '9', 'a'), (r0 + 1, 'a', '9')):
            for c in (nc0, nc0 + 1):
                if g[r][c] != head_col:
                    g[r][c] = head_col
                    changes[f"{r},{c}"] = head_col
            for c in (nc0 + 2, nc0 + 3):
                if g[r][c] != tail_col:
                    g[r][c] = tail_col
                    changes[f"{r},{c}"] = tail_col

    def toggle_player_colors(g, changes):
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        for r in (r0, r0 + 1):
            for c in range(c0, c0 + 4):
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
