def predict(probe):
    # Beliefs (v16):
    # - Grid 64x64 hex. Colours: 5 background, 2/9/a player, e/0/2 blocks, 3 walls.
    # - Top-right cols 62-63 is a timer bar: fills with 0 from top, 2 rows per tick.
    #   Bar reaching row 63 => next action causes GAME_OVER [E14,E15].
    # - ACTION1/ACTION3 do NOT move the player. They toggle the player's internal
    #   9<->a pattern (swap the 9 and a sub-blocks) [E24 step1, E13, E14].
    # - ACTION2/ACTION4 also toggle the player's 9<->a pattern [E2,E4,E11,E19].
    # - Bar tick timing is irregular: not every action ticks [E24: steps 1,4 no tick;
    #   E13: steps 2,5 no tick; E12: all tick]. Modeled as: tick on most actions,
    #   but ACTION1/ACTION3 tick only ~every other action (approximate, marked ?).
    # - CLICK on a 3x3 block region cycles its colour e->0->2->e [E18,E20,E22,E23].
    #   Each block-click ticks the bar [E8,E18,E19,E20,E21,E22,E23].
    # - CLICK elsewhere: no change, no tick [E17,E21(15,20)].
    # - Block regions: 3x3 at row-bands {49-51,54-56,59-61} x col-bands {24-26,29-31,34-36}.
    # - RESET restores initial state [E16].
    #
    # GOAL (?): unknown. Best guess: set all blocks to a target colour before the
    # timer bar fills. Marked uncertain.

    actions = probe.get("actions", [])
    frame = probe.get("frame", None)

    steps = []

    if frame is not None:
        grid = [list(row) for row in frame]
    else:
        grid = [['5'] * 64 for _ in range(64)]

    # Timer bar fill: count leading rows where both cols 62,63 are '0'
    bar_fill = 0
    for r in range(64):
        if grid[r][62] == '0' and grid[r][63] == '0':
            bar_fill += 1
        else:
            break

    # Player region: rows 19-22, cols 35-42. Toggle swaps 9<->a within it.
    player_rows = range(19, 23)
    player_cols = range(35, 43)

    def toggle_player(changes):
        for r in player_rows:
            for c in player_cols:
                cur = grid[r][c]
                if cur == '9':
                    grid[r][c] = 'a'
                    changes[f"{r},{c}"] = 'a'
                elif cur == 'a':
                    grid[r][c] = '9'
                    changes[f"{r},{c}"] = '9'

    # Block regions: (row0, col0) top-left of each 3x3 block
    block_regions = []
    for r0 in (49, 54, 59):
        for c0 in (24, 29, 34):
            block_regions.append((r0, c0))

    def tick(changes):
        nonlocal bar_fill
        for _ in range(2):
            if bar_fill < 64:
                changes[f"{bar_fill},62"] = '0'
                changes[f"{bar_fill},63"] = '0'
                bar_fill += 1

    state = "NOT_FINISHED"
    levels_done = 0
    # parity counter for ACTION1/ACTION3 bar-tick approximation (?)
    move_count = 0

    for act in actions:
        changes = {}

        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
                bar_fill = 0
                move_count = 0
                for r in range(64):
                    changes[f"{r},62"] = 'e'
                    changes[f"{r},63"] = 'e'
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act == "RESET":
            bar_fill = 0
            move_count = 0
            state = "NOT_FINISHED"
            for r in range(64):
                changes[f"{r},62"] = 'e'
                changes[f"{r},63"] = 'e'
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION1", "ACTION3"):
            toggle_player(changes)
            # ? bar ticks on roughly every other move action
            move_count += 1
            if move_count % 2 == 0:
                tick(changes)
            if bar_fill >= 64:
                state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION2", "ACTION4"):
            toggle_player(changes)
            tick(changes)
            if bar_fill >= 64:
                state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                steps.append({"changes": {}, "levels": levels_done, "state": state})
                continue
            hit = False
            for (r0, c0) in block_regions:
                if r0 <= y <= r0 + 2 and c0 <= x <= c0 + 2:
                    cur = grid[y][x] if (0 <= y < 64 and 0 <= x < 64) else 'e'
                    # cycle e->0->2->e
                    if cur == 'e':
                        new = '0'
                    elif cur == '0':
                        new = '2'
                    elif cur == '2':
                        new = 'e'
                    else:
                        new = '0'
                    for rr in range(r0, r0 + 3):
                        for cc in range(c0, c0 + 3):
                            changes[f"{rr},{cc}"] = new
                            if 0 <= rr < 64 and 0 <= cc < 64:
                                grid[rr][cc] = new
                    hit = True
                    break
            if hit:
                tick(changes)
                if bar_fill >= 64:
                    state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        steps.append({"changes": {}, "levels": levels_done, "state": state})

    return {"steps": steps}
