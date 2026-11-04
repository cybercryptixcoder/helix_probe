def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   successful action [E2,E4,E12,E18,E22,E23,E24,E25,E26,E37,E38,E44].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15,E35].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29].
    # - Clickable 3x3 blocks cycle colour e->0->2->e [E18,E20,E22,E23,E41,E43].
    # - ACTION3 moves the player LEFT by 4 columns per press [E37,E38,E44].
    #   E44: 6 ACTION3 from start (head c39-40): c35-36, c31-32, c27-28, c23-24, then stuck.
    #   That's 4 cols/press until hitting left edge c23. E37: 2 presses -> c35-36 (4 cols).
    #   E38: 2 presses -> c31-32 (8 cols from c39-40). So 4 cols/press. Confirmed.
    # - ACTION1 moves the player RIGHT by 4 columns per press [E28,E30,E32].
    #   E30: ACTION1 at left edge c23 did nothing. Then ACTION3 moved to c23-24 (LEFT).
    #   E28: [A1,A3,A3,A1] from c39-40: A1->c37-38? That's LEFT. Hmm.
    #   Actually E28 step1 A1 -> c37-38:9 (LEFT 2?). Let me use E44 as ground truth for A3.
    #   For A1, E32: [A3,A3,A1,A1,A1] from c39-40. Step1 A3->c35-36 (LEFT4). Step2 A3->c31-32 (LEFT4).
    #   Step3 A1->c25-26 (LEFT6?). Step4 A1->0 changes. Step5 A1->0 changes.
    #   Messy. Best guess: ACTION1 = RIGHT 4, ACTION3 = LEFT 4. Mark "?".
    # - Player sprite: 4 wide, 4 tall. Head 2 cols (top 9, bottom a), tail 2 cols (top a, bottom 9).
    #   Moving shifts whole sprite; vacated cells become 2 [E37,E38,E44].
    # - ACTION2 toggles player's 9/a colours in place, no shift [E25,E26,E40].
    #   E40: ACTION2 toggled colours in place. E42: ACTION2 did nothing (0 changes) then bar advanced.
    #   Wait E42: ACTION2 -> 0 changes, ACTION2 -> bar only. So ACTION2 sometimes does nothing?
    #   E40: ACTION2 -> toggled r19-20 c31-34. Hmm. E42 at "after":15, ACTION2 -> 0 changes.
    #   Maybe ACTION2 toggles only when player is in a certain state. Mark "?".
    # - ACTION4 moves player LEFT 4 and toggles colours [E39,E42].
    #   E42: ACTION4 -> c31-34:2, c35-36:a, c37-38:9 (moved right? from c31-32 to c35-36 = RIGHT4).
    #   E39: ACTION4 -> c27-30:2, c31-32:a, c33-34:9 (from c31-32 to c33-34 = RIGHT2?).
    #   Mark "?" - ACTION4 = RIGHT 4 + toggle.
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
        # direction: -1 = left, +1 = right; moves 4 cols
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        nc0 = c0 + direction * 4
        if nc0 < 23 or nc0 + 3 > 42:
            return
        for r in (r0, r0 + 1):
            for c in range(c0, c0 + 4):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
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
            shift_player(grid, +1, changes)
            successful = True
        elif act == "ACTION3":
            shift_player(grid, -1, changes)
            successful = True
        elif act == "ACTION2":
            toggle_player_colors(grid, changes)
            successful = True
        elif act == "ACTION4":
            shift_player(grid, +1, changes)
            toggle_player_colors(grid, changes)
            successful = True

        if successful:
            filled_before = bar_filled_rows(grid)
            advance_bar(grid, changes)
            if filled_before >= ROWS:
                state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
