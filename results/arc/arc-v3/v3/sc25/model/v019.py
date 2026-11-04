def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   "successful" action [E2,E4,E12,E18,E22,E23,E24,E25,E26].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29].
    # - Clickable 3x3 blocks toggle colour among e/0/2 [E5,E18,E20,E22,E23].
    #   Cycle order e->2->0->e (observed on repeated clicks) [E22,E23].
    # - ACTION1/ACTION3 move the player block horizontally by 2 cols [E13,E14,E24,E27,E28].
    #   The player is a 2x2 "head" (9/a) plus a trailing 2x2 "tail" (a/9) that lags
    #   one step behind, leaving a 2x2 "2" trail behind the tail [E27,E28].
    #   Actually: player is a 2x2 block; ACTION3 moves it right 2, ACTION1 left 2.
    #   The 9/a colours are fixed: top row 9, bottom row a for the head; the tail
    #   (previous position) shows the opposite (a top, 9 bottom) then becomes 2 [E27,E28].
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
        # Move the 2x2 player head left/right by 2 cols.
        # Head colours: top row 9, bottom row a (fixed orientation).
        # The vacated 2x2 becomes 2 (trail). Old trail cells become 2 too.
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        nc0 = c0 + direction * 2
        if nc0 < 23 or nc0 + 1 > 42:
            return
        # clear old head cells to 2
        for r in (r0, r0 + 1):
            for c in (c0, c0 + 1):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
        # write new head: top row 9, bottom row a
        for r, col in ((r0, '9'), (r0 + 1, 'a')):
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
