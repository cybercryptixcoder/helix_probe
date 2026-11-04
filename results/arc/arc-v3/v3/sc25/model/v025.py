def predict(probe):
    # Beliefs (with evidence):
    # - Right column c62-63 is a budget/timer bar filled with 0 from top, 2 rows per
    #   successful action [E2,E4,E12,E18,E22,E23,E24,E25,E26,E37,E38,E44].
    # - When bar is full (all rows 0-63 = 0), the next successful action -> GAME_OVER [E14,E15,E35].
    # - Invalid clicks on empty space change nothing and do NOT advance the bar [E1,E17,E21,E25,E29,E47].
    # - Clickable 3x3 blocks cycle colour e->0->2->e [E18,E20,E22,E23,E41,E43].
    #   E41: block (30,55) '0'->'e'. E43: (30,50) '0'->'e', (25,55) '0'->'e'.
    #   E39: (30,50) 'e'->'0'. E47: (30,50) 'e'->'0'. E35: (30,55) '0'->'2'.
    #   So cycle is e->0->2->e. (0->e would contradict E35 0->2; use e->0->2->e.)
    # - Player sprite: 4 wide x 4 tall, left 2 cols 9, right 2 cols a [E44,E46].
    # - ACTION3 moves player LEFT 4 cols per press [E37,E38,E44].
    #   E44: 6 presses from c39-42: c35-38, c31-34, c27-30, c23-26, then stuck (edge c23).
    # - ACTION1 moves player RIGHT 4 cols per press [E28,E30,E32,E46].
    #   E46: from c23-26, ACTION1 -> c25-26:9 / c23-24:a (12 cells). Hmm that's odd.
    #   E46 step3: r19-20 c25-26:9, r21-22 c23-24:a. That's a partial sprite, not full 4x4.
    #   Actually E46 step3 shows only 12 cells: r19-20 c25-26:9 and r21-22 c23-24:a.
    #   This looks like the sprite is 2x2 head (9) + 2x2 tail (a), head at c25-26, tail at c23-24.
    #   Wait — E44 clearly showed 4x4 with left-2=9 right-2=a across all 4 rows.
    #   E46 step3 contradicts: only 12 cells, head top-2-rows c25-26, tail bottom-2-rows c23-24.
    #   Reconcile: maybe sprite is 2x2 head (9) at top, 2x2 tail (a) at bottom, offset.
    #   E44 step1: r19 c35-36:9, r19 c37-38:a, r20 c35-36:9, r20 c37-38:a, r21 c35-36:9, r21 c37-38:a, r22 same.
    #   That's ALL 4 rows having c35-36:9 and c37-38:a. So 4x4 with left-2=9, right-2=a.
    #   E46 step3: r19-20 c25-26:9, r21-22 c23-24:a. That's head 2x2 at top-right, tail 2x2 at bottom-left.
    #   These are different! Unless E46 step3 is a transition. Let me re-read E46.
    #   E46: after=31, actions [A3,A3,A1,A1]. Step1: bar only (r32-33). Step2: 0 changes.
    #   Step3 (A1): 12 cells r19-20 c25-26:9, r21-22 c23-24:a, bar r34-35.
    #   Step4 (A1): bar only r36-37.
    #   So at after=31, player was at c23-26 (from E44's 6 A3 ending at c23-26).
    #   Wait E44 ended at c23-26 (4th press), then 5th/6th stuck. So after=28 player at c23-26.
    #   Then E45 (after=28): CLICK, A3, CLICK. A3 at c23-26 stuck (edge). So still c23-26 at after=31.
    #   E46 step1 A3: stuck (c23-26), bar only. Step2 A3: stuck, 0 changes. 
    #   Step3 A1: moves RIGHT. From c23-26 to... c25-26:9 (head) + c23-24:a (tail)?
    #   That doesn't make sense as a move right. Unless the sprite is head 2x2 + tail 2x2 diagonal.
    #   Hmm. Let me reconsider the sprite shape entirely.
    #   E44 step1 (after 1 A3 from c39-42): r19-22 all have c35-36:9, c37-38:a. 4x4 block.
    #   E44 step4 (after 4 A3): r19-22 all have c23-24:9, c25-26:a. 4x4 block.
    #   So sprite IS 4x4: left-2=9, right-2=a. Confirmed by E44.
    #   E46 step3: r19-20 c25-26:9, r21-22 c23-24:a. This is NOT a 4x4 block.
    #   This is 2x2 head (9) at top, 2x2 tail (a) at bottom, horizontally offset by 2.
    #   Contradiction with E44. Unless... E46 step3 is a partial render / the sprite changed shape.
    #   OR: E46 step3 shows the sprite moving right from c23-26: new head at c25-26 (9), 
    #   and the tail (a) is being left behind at c23-24 but only bottom rows? 
    #   This is confusing. Given E44 is very clear (4x4, left-2=9, right-2=a), I'll trust that.
    #   E46 step3 might be a rendering where the sprite is 2x2 head + 2x2 tail arranged diagonally.
    #   Actually — maybe the sprite is: head 2x2 (9) at top, tail 2x2 (a) at bottom, and they
    #   are offset. In E44 step1: head at top c35-36 (9), tail at bottom c37-38 (a)? 
    #   No, E44 shows all 4 rows with c35-36:9 and c37-38:a. So it's a solid 4x4.
    #   I'll go with 4x4 left-2=9 right-2=a, and treat E46 step3 as anomalous (maybe a 
    #   transition frame). Mark "?".
    # - ACTION2 toggles player's 9/a colours in place, but only sometimes [E25,E26,E40,E42].
    #   E40: A2 toggled (12 cells), then A2 did nothing, then A2 nothing, then bar only.
    #   E42: A2 did nothing, A2 bar only, A4 moved+toggled, A4 moved+toggled.
    #   So ACTION2 toggles only if... maybe it toggles the sprite's orientation state.
    #   Best guess: ACTION2 toggles 9<->a in place. Mark "?".
    # - ACTION4 moves player RIGHT 4 and toggles colours [E39,E42].
    #   E42: A4 moved c31-34 to c35-38, colours c35-36:a, c37-38:9 (toggled). Confirmed.
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
        # cycle e->0->2->e [E18,E20,E22,E23,E39,E41,E43,E47]
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
