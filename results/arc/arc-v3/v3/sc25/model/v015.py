def predict(probe):
    # Beliefs (v15):
    # - Grid 64x64 hex. Colours: 5 background, 2/9/a player, e/0/2 blocks, 3 walls.
    # - Top-right cols 62-63 is a timer bar: fills with 0 from top, 2 rows per "tick".
    #   A tick happens on most actions but NOT every action [E13,E14: some actions no bar].
    #   Bar reaching row 63 => GAME_OVER [E15].
    # - ACTION1/ACTION3 move the player block left/right by 2 cols AND tick the bar [E10,E12,E13,E14].
    # - ACTION2/ACTION4 toggle player internal 9<->a colours AND tick the bar [E2,E4,E11,E19].
    # - CLICK on a 3x3 block region cycles its colour e->0->2->e (3-cycle) [E18,E20].
    #   Each click that hits a block also ticks the bar [E8,E9,E18,E19,E20,E21].
    # - CLICK elsewhere: no change, no tick [E17,E9(40,21),E21(15,20)].
    # - Block regions are 3x3 at (col,row) anchors: (29,49),(29,54),(24,54),(24,59),(34,54),(34,59)...
    #   Actually observed block cells: rows 49-51 c29-31; rows 54-56 c29-31; rows 54-56 c24-26;
    #   rows 59-61 c24-26; rows 54-56 c34-36. So blocks at row-bands {49-51,54-56,59-61} x col-bands {24-26,29-31,34-36}.
    # - RESET restores initial state [E16].
    #
    # GOAL (?): unknown. Best guess: set all blocks to a target colour (e.g. all 'e' or all '0')
    # before the timer bar fills. Marked uncertain.

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

    # Player left edge (leftmost 2 in rows 19-22)
    player_left = 35
    for r in range(19, 23):
        for c in range(64):
            if grid[r][c] == '2':
                player_left = c
                break
        else:
            continue
        break

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

    for act in actions:
        changes = {}

        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
                bar_fill = 0
                player_left = 35
                # approximate: clear bar
                for r in range(64):
                    changes[f"{r},62"] = 'e'
                    changes[f"{r},63"] = 'e'
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act == "RESET":
            bar_fill = 0
            player_left = 35
            state = "NOT_FINISHED"
            for r in range(64):
                changes[f"{r},62"] = 'e'
                changes[f"{r},63"] = 'e'
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION1", "ACTION3"):
            if act == "ACTION1":
                player_left = max(0, player_left - 2)
            else:
                player_left = min(56, player_left + 2)
            tick(changes)
            if bar_fill >= 64:
                state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION2", "ACTION4"):
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
