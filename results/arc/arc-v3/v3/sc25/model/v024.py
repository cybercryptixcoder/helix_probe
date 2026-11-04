def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   successful action [E2,E4,E12,E18,E22,E23,E24,E25,E26,E37,E38,E44].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15,E35].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29].
    # - Clickable 3x3 blocks cycle colour e->0->2->e [E18,E20,E22,E23,E41,E43].
    #   E41: block at (30,55) was '0' -> became 'e' (0->e). E43: (30,50) '0'->'e', (25,55) '0'->'e'.
    #   So cycle is e->0->2->e? E41 shows 0->e, E43 shows 0->e. Hmm, that's 0->e not 0->2.
    #   Wait: E41 block was at '0' (from earlier clicks) and became 'e'. E43 same.
    #   E18: 4 clicks on (30,50). E20: 2 clicks on (30,55) then 2 on (25,55).
    #   Let me reconsider: maybe cycle is 0->e->2->0? E41: 0->e. E43: 0->e. 
    #   E35: (30,55) was '0' -> became '2'. That contradicts 0->e!
    #   Hmm E35: block (30,55) '0'->'2'. E41: (30,55) '0'->'e'. Different results from same colour?
    #   Maybe the block cycles based on click count/history, OR the initial colour differs.
    #   Actually E35 was at "after":59, E41 at "after":14. Different level states.
    #   Let me just use: cycle e->0->2->e as before but note E41/E43 show 0->e directly.
    #   Best guess: cycle is 0->e->2->0 (i.e. 0->e, e->2, 2->0). E35 0->2 contradicts.
    #   Mark "?" - keep e->0->2->e but E41/E43 suggest 0->e. Try 0->e->2->0.
    #   Actually E18: 4 clicks. If cycle 0->e->2->0: start? unknown. Let's keep simple e->0->2->e
    #   but the E41/E43 evidence (0->e) is strong. Use cycle: 0->e, e->2, 2->0. Mark "?".
    # - ACTION3 moves the player LEFT by 4 columns per press [E37,E38,E44].
    #   E44: 6 ACTION3 from start (head c39-40): c35-36, c31-32, c27-28, c23-24, then stuck.
    #   That's 4 cols/press until hitting left edge c23. Confirmed.
    # - ACTION1 moves the player RIGHT by 4 columns per press [E28,E30,E32].
    #   E32: [A3,A3,A1,A1,A1] from c39-40. Step1 A3->c35-36 (LEFT4). Step2 A3->c31-32 (LEFT4).
    #   Step3 A1->c25-26 (LEFT6?). Hmm that's odd. Actually observed E32 step3: r19 c25-26:9, r20 c25-26:9,
    #   r21 c23-24:a, r22 c23-24:a. That's head at c25-26, tail at c23-24. So player at c23-26.
    #   From c31-32 (head) to c23-26: that's LEFT 8? Or the player is 4 wide c23-26.
    #   Wait the sprite: head 2 cols + tail 2 cols = 4 wide. At c31-32 head means sprite c31-34.
    #   After A1: sprite at c23-26. That's LEFT 8. But A1 should be RIGHT. Contradiction.
    #   Hmm. Maybe ACTION1 = LEFT 8? Or the sprite layout differs.
    #   E32 step3 shows only r19-20 c25-26:9 and r21-22 c23-24:a changed (12 cells). 
    #   Actually maybe A1 moves LEFT by 8 when near edge? This is messy.
    #   Let me reconsider E44: A3 moves LEFT 4. E37: 2 A3 -> c35-36 (4 cols from c39-40). Confirmed LEFT4.
    #   For A1: E30 said A1 at left edge did nothing. E28: [A1,A3,A3,A1] from c39-40.
    #   E28 step1 A1 -> c37-38:9 (from comments). That's LEFT 2? 
    #   Given confusion, best guess: ACTION1 = RIGHT 4, ACTION3 = LEFT 4. Mark "?".
    # - Player sprite: 4 wide, 4 tall. Head 2 cols (top 9, bottom a), tail 2 cols (top a, bottom 9).
    #   E44 confirms: at c35-36 head (r19-20:9, r21-22:9? no). Let me read E44 step1:
    #   r19 c35-36:9, r19 c37-38:a, r20 c35-36:9, r20 c37-38:a, r21 c35-36:9, r21 c37-38:a, r22 same.
    #   So ALL rows r19-22 have c35-36:9 and c37-38:a. That's a 4x4 block: left 2 cols 9, right 2 cols a.
    #   So sprite is 4 wide x 4 tall, left half 9, right half a. NOT head/tail vertical.
    #   E44 step2: c31-32:9, c33-34:a all rows. Confirmed: left 2 cols 9, right 2 cols a.
    #   So sprite = 4x4, cols [c0,c1]=9, [c2,c3]=a, all 4 rows.
    # - ACTION2 toggles player's 9/a colours in place [E25,E26,E40].
    #   E40: ACTION2 -> toggled r19-20 c31-34 (12 cells: r19 c33-34:a, r20 c33-34:a, r21 c31-32:9, r22 c31-32:9).
    #   Wait that's swapping 9<->a. E40 step1: r19 c33-34:a (was 9), r20 c33-34:a, r21 c31-32:9 (was a), r22 c31-32:9.
    #   So it toggled: left cols became a, right cols became 9. Full 4x4 toggle.
    #   E40 step2: 0 changes (bar only). E40 step3: 0 changes. E40 step4: bar only.
    #   So ACTION2 toggles once then does nothing? Or toggles every other press?
    #   E42: ACTION2 -> 0 changes, ACTION2 -> bar only. So ACTION2 sometimes does nothing.
    #   Maybe ACTION2 toggles only if not already toggled? Or it's a state thing.
    #   Best guess: ACTION2 toggles 9<->a in place. Mark "?".
    # - ACTION4 moves player RIGHT 4 and toggles colours [E39,E42].
    #   E42: ACTION4 -> sprite moved from c31-34 to c35-38, colours: c35-36:a, c37-38:9 (toggled).
    #   So ACTION4 = RIGHT 4 + toggle. E39: ACTION4 -> c31-32:a, c33-34:9 (from c27-30 to c31-34 = RIGHT4, toggled).
    #   Confirmed: ACTION4 = RIGHT 4 + toggle.
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
        # "?" cycle: 0->e, e->2, 2->0 (E41,E43 show 0->e; E35 shows 0->2 contradiction)
        order = {'0': 'e', 'e': '2', '2': '0'}
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
        # sprite is 4x4, left 2 cols 9, right 2 cols a (or toggled)
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
        # clear old sprite (4x4 -> 2)
        for r in range(r0, r0 + 4):
            for c in range(c0, c0 + 4):
                if g[r][c] in ('9', 'a'):
                    g[r][c] = '2'
                    changes[f"{r},{c}"] = '2'
        # draw new sprite: left 2 cols 9, right 2 cols a
        for r in range(r0, r0 + 4):
            for c in (nc0, nc0 + 1):
                if g[r][c] != '9':
                    g[r][c] = '9'
                    changes[f"{r},{c}"] = '9'
            for c in (nc0 + 2, nc0 + 3):
                if g[r][c] != 'a':
                    g[r][c] = 'a'
                    changes[f"{r},{c}"] = 'a'

    def toggle_player_colors(g, changes):
        pos = find_player(g)
        if pos is None:
            return
        r0, c0 = pos
        for r in range(r0, r0 + 4):
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
