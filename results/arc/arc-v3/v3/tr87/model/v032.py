def predict(probe):
    # Beliefs:
    # - Grid has 5 "sockets" at cols (15-19),(22-26),(29-33),(36-40),(43-47), rows 48-60.
    #   The active socket is the one with '0' on its top border (r48) [E1,E56,E59].
    # - ACTION3 / ACTION4 move the active socket: ACTION4 -> next (right), ACTION3 -> prev (left);
    #   the old socket's border becomes '3', the new one's becomes '0' [E56,E59,E60].
    # - ACTION1 / ACTION2 rotate the 5x5 interior (rows 52-56) of the active socket
    #   (ACTION1 = 90 CW, ACTION2 = 90 CCW) — best guess, imperfect [E63,E64,E67].
    # - Progress bar: rightmost '4' in row 63. It moves LEFT by 1 ONLY on ACTION1/ACTION2,
    #   NOT on ACTION3/ACTION4/RESET [E34,E59,E60,E61,E63,E67]. Reaching 0 => GAME_OVER (?).
    # - RESET restarts the level (bar back to full, active socket back to first) (?).
    # - GOAL guess (?): maybe when all interiors match / some target pattern. Unknown.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", [])

    grid = [list(row) for row in frame] if frame else [['2'] * 64 for _ in range(64)]

    sockets = [(15, 19), (22, 26), (29, 33), (36, 40), (43, 47)]

    # active socket: the one with '0' at row 48
    active = 0
    for i, (cs, ce) in enumerate(sockets):
        if grid[48][cs] == '0':
            active = i
            break

    # progress bar: rightmost '4' in row 63
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
            # reset progress bar to full
            for c in range(64):
                if grid[63][c] == '4':
                    grid[63][c] = '1'
                    changes[f"63,{c}"] = '1'
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
            # rotate 5x5 interior of active socket
            cs, ce = sockets[active]
            sub = [[grid[r][c] for c in range(cs, ce + 1)] for r in range(52, 57)]
            if a == "ACTION1":
                new = [[sub[4 - j][i] for j in range(5)] for i in range(5)]  # CW
            else:
                new = [[sub[j][4 - i] for j in range(5)] for i in range(5)]  # CCW
            for i in range(5):
                for j in range(5):
                    r = 52 + i
                    c = cs + j
                    if grid[r][c] != new[i][j]:
                        grid[r][c] = new[i][j]
                        changes[f"{r},{c}"] = new[i][j]
            # progress bar moves left by 1 on ACTION1/ACTION2 only
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
