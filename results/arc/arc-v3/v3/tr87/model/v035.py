def predict(probe):
    # Border/socket movement: ACTION4 -> next socket, ACTION3 -> prev; old border '3', new '0' [E56,E59,E60,E69,E71]
    # Progress bar: rightmost '4' in row 63 moves LEFT by 1 on ACTION1/ACTION2 [E63,E64,E66,E67,E70,E73,E75]; not on ACTION3/ACTION4 [E69,E71]
    #   ...but RESET does NOT move the bar [E76: RESET step changed many cells but no r63 '4' move]
    # Interior: ACTION1/ACTION2 toggle 5<->7 on a content-dependent subset of the active 5x5 interior (? uncertain) [E64,E65,E68,E72,E74]
    # RESET: restores the whole level to its initial layout (all tiles' interiors, borders, bar) [E76]
    # GOAL (?): unknown; likely matching interiors to a target. Bar reaching 0 => GAME_OVER (?).

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    grid = [list(row) for row in frame] if frame else [['2'] * 64 for _ in range(64)]
    sockets = [(15, 19), (22, 26), (29, 33), (36, 40), (43, 47)]

    active = 0
    for i, (cs, ce) in enumerate(sockets):
        if grid[48][cs] == '0':
            active = i
            break

    prog = 0
    for c in range(63, -1, -1):
        if grid[63][c] == '4':
            prog = c
            break

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    def set_border(idx, val, changes):
        cs, ce = sockets[idx]
        for r in (48, 49, 59, 60):
            for c in range(cs, ce + 1):
                if r in (48, 60) or c in (cs, ce):
                    if grid[r][c] in ('0', '3') and grid[r][c] != val:
                        grid[r][c] = val
                        changes[f"{r},{c}"] = val

    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            if a == "RESET":
                prog = 63
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if a == "RESET":
            for i, (cs, ce) in enumerate(sockets):
                want = '0' if i == 0 else '3'
                set_border(i, want, changes)
            active = 0
            prog = 63
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if a == "ACTION4":
            set_border(active, '3', changes)
            active = (active + 1) % 5
            set_border(active, '0', changes)

        elif a == "ACTION3":
            set_border(active, '3', changes)
            active = (active - 1) % 5
            set_border(active, '0', changes)

        elif a in ("ACTION1", "ACTION2"):
            cs, ce = sockets[active]
            for r in range(52, 57):
                for c in range(cs, ce + 1):
                    if grid[r][c] == '5':
                        grid[r][c] = '7'
                        changes[f"{r},{c}"] = '7'
                    elif grid[r][c] == '7':
                        grid[r][c] = '5'
                        changes[f"{r},{c}"] = '5'
            if prog > 0:
                old = prog
                prog -= 1
                if grid[63][prog] != '4':
                    grid[63][prog] = '4'
                    changes[f"63,{prog}"] = '4'
                if grid[63][old] == '4':
                    grid[63][old] = '1'
                    changes[f"63,{old}"] = '1'
                if prog == 0:
                    state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
