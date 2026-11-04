def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   successful action [E2,E4,E12,E18,E22,E23,E24,E25,E26,E37,E38].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15,E35].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29].
    # - Clickable 3x3 blocks cycle colour e->0->2->e [E18,E20,E22,E23,E41].
    #   E41: clicking a block currently '0' -> 'e'. E39: clicking 'e' -> '0'. So cycle is e->0->2->e.
    # - ACTION1/ACTION3 move the player LEFT/RIGHT by 2 cols per press [E27,E28,E30,E32,E34,E38].
    #   E30: ACTION1 at left edge (c23) does nothing (0 changes). E32: ACTION3 at right edge does nothing.
    # - The player is a 4-wide, 4-tall sprite: head 2 cols (top 9, bottom a), tail 2 cols
    #   (top a, bottom 9). Moving shifts whole sprite by 2 cols; vacated cells become 2 [E27,E28,E38].
    #   Initial head at c39-40, tail at c41-42 [E36]. Wait E38: after 2 ACTION3 from start, sprite at
    #   c27-34 (head c27-28, tail c29-30, trail 2 at c31-34). So each ACTION3 moves LEFT by 4 cols?
    #   E38 after 2 presses: head c27-28. Start head c39-40. Moved 12 cols in 2 presses = 6/press? No.
    #   Actually E37: 2 ACTION3 -> head c35-36 (from c39-40 = 4 cols left in 2 presses = 2/press).
    #   E38: 2 ACTION3 -> head c27-28. That's 12 cols in 2 presses. Inconsistent unless state differs.
    #   E38 "after":4 means 4 actions already used. Hmm. Let me use: ACTION3 moves LEFT 2 cols/press.
    #   E37 after 2 ACTION3: c39-40 -> c35-36 = 4 cols = 2/press. Good.
    #   E38 after 2 ACTION3: c39-40 -> c27-28 = 12 cols. Contradiction. "after":4 - maybe 2 prior moves.
    #   I'll model ACTION3 = left 2, ACTION1 = right 2 (E28: ACTION1 then ACTION3 then ACTION3 then ACTION1).
    #   E28: start c39-40. A1->c37-38 (right? no, c37 is left). Hmm E28 A1 gave c37-38:9 = moved LEFT 2.
    #   So ACTION1 = LEFT 2, ACTION3 = RIGHT 2? But E30 ACTION1 at c23 did nothing (left edge).
    #   E30: after 42, ACTION1 -> 0 changes (at left edge c23). ACTION3 -> c23-24 (moved left to edge).
    #   Wait E30 ACTION3 moved to c23-24 from c25-26 = LEFT 2. So ACTION3 = LEFT.
    #   E28: A1 -> c37-38 (from c39-40, LEFT 2). So ACTION1 = LEFT too?? 
    #   Let me recheck E28: [A1,A3,A3,A1]. Step1: c37-38:9 (LEFT 2). Step2: c31-32:9 (LEFT 6 more).
    #   Step3: c27-28:9 (LEFT 4). Step4: c29-30:9 (RIGHT 2). So A1=LEFT2, A3=LEFT? 
    #   Step2 A3 moved c37->c31 = LEFT 6. Step3 A3 moved c31->c27 = LEFT 4. Step4 A1 moved c27->c29 = RIGHT 2.
    #   This is messy. Given time, model: ACTION1 = LEFT 2, ACTION3 = RIGHT 2 (best simple guess), "?".
    # - ACTION2/ACTION4 toggle the player's 9/a colours in place (no shift) [E25,E26,E40].
    #   E40: ACTION2 toggled colours (a<->9) in place, no shift. E39: ACTION4 moved left 8 + toggled "?".
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
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        nc0 = c0 + direction * 2
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

    def move_and_toggle(g, steps, changes):
        for _ in range(steps):
            shift_player(g, -1, changes)
        toggle_player_colors(g, changes)

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
        elif act == "ACTION2":
            toggle_player_colors(grid, changes)
            successful = True
        elif act == "ACTION4":
            move_and_toggle(grid, 4, changes)
            successful = True

        if successful:
            filled_before = bar_filled_rows(grid)
            advance_bar(grid, changes)
            if filled_before >= ROWS:
                state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
