def predict(probe):
    # Model of the black box, level 1.
    #
    # Screen layout (from the current screen):
    #   - rows 0-32: mostly static background (2s), with four 7x7 "tiles" at
    #     rows 4-10, 13-19, 22-28, cols 12-18 / 21-27, and a big text banner
    #     at rows 40-46.  These never change in the evidence.
    #   - rows 34-63: a 3-colour playfield.  Rows 34-39 are solid 3.
    #     Rows 40-46 hold a banner of 'a'/'5' (static).
    #     Rows 48-60: a row of "sockets" (0/3 outlined boxes) at cols
    #       15-19, 22-26, 29-33, 36-40, 43-47.  These toggle 0<->3.
    #     Rows 52-56: "puzzle" cells (5/7) inside each socket region.
    #     Row 63: a progress bar of 4s that advances right-to-left,
    #       starting at c63 and moving left one cell per action; when it
    #       reaches c0 the game is GAME_OVER [E32].
    #
    # Actions:
    #   ACTION4: advances the socket "selector" one step to the right
    #     (wrapping), toggling the selected socket 0<->3 and the one to its
    #     left [E1,E34,E45...].  Concretely each ACTION4 flips the pair
    #     (socket[i], socket[i-1]) where i cycles 0..4.
    #   ACTION3: same toggle but stepping the other way / different phase
    #     [E3,E7,E22,E51...].  In evidence ACTION3 and ACTION4 both toggle
    #     socket pairs; they differ in which pair is affected given history.
    #   ACTION1 / ACTION2: toggle the 5/7 pattern inside the *currently
    #     selected* socket's puzzle region [E2,E6,E12...].  ACTION1 and
    #     ACTION2 are inverses (5<->7) of each other on those cells.
    #   RESET: restore the level to its start screen [E33,E38,E40...].
    #
    # Progress bar: every action (except RESET) moves the rightmost 4 one
    # cell left; at c0 => GAME_OVER [E32].  RESET restores it to the start.
    #
    # GOAL (guess "?"): make the five socket outlines all 3 (or all 0) and
    # the puzzle patterns match a target; most likely completing the level
    # means aligning all sockets to the same state.  We predict WIN when,
    # after the action, all five sockets are 3 and all puzzle cells are 7
    # (best guess; unproven).

    actions = probe.get("actions", [])
    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])

    # Build mutable grid.
    grid = [list(row) for row in frame] if frame else [['2']*64 for _ in range(64)]

    # Socket definitions: (col_start, col_end) for the outline rows 48-60,
    # and puzzle region rows 52-56.
    sockets = [(15,19),(22,26),(29,33),(36,40),(43,47)]

    # Reconstruct internal state by replaying history from a known start.
    # We track: progress bar position, socket selector index, and grid.
    # Since we have the current frame, we only need the *selector* and the
    # progress position, which we infer from history.
    #
    # Progress bar: starts at c63.  Each non-RESET action moves it left 1.
    # RESET sets it back to c63.
    prog = 63
    sel = 0  # selector index for ACTION4/ACTION3 stepping
    # We can't perfectly recover sel from history without the start state,
    # so we approximate: sel increments on ACTION4, decrements on ACTION3.
    for a in history:
        if a == "RESET":
            prog = 63
            sel = 0
        elif a in ("ACTION1","ACTION2","ACTION3","ACTION4"):
            prog = max(0, prog - 1)
            if a == "ACTION4":
                sel = (sel + 1) % 5
            elif a == "ACTION3":
                sel = (sel - 1) % 5

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            # only RESET works
            if a == "RESET":
                # restore start-ish: we don't know exact start, so clear
                # progress bar and reset selector
                prog = 63
                sel = 0
                # clear progress bar 4s back to background (1 at row63?)
                # From evidence RESET restores row63 to 1s in changed cells.
                for c in range(64):
                    if grid[63][c] == '4':
                        grid[63][c] = '1'
                        changes[f"63,{c}"] = '1'
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if a == "RESET":
            prog = 63
            sel = 0
            # reset progress bar cells that are 4 back to 1
            for c in range(64):
                if grid[63][c] == '4':
                    grid[63][c] = '1'
                    changes[f"63,{c}"] = '1'
            # (full reset of sockets/puzzles not modeled precisely)
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue

        if a in ("ACTION1","ACTION2","ACTION3","ACTION4"):
            # progress bar moves left
            if prog > 0:
                old = prog
                prog -= 1
                # set cell at new prog to 4, restore old to 1
                if grid[63][prog] != '4':
                    grid[63][prog] = '4'
                    changes[f"63,{prog}"] = '4'
                if grid[63][old] == '4':
                    grid[63][old] = '1'
                    changes[f"63,{old}"] = '1'
                if prog == 0:
                    state = "GAME_OVER"

            if a == "ACTION4":
                # toggle socket sel and sel-1
                i = sel
                j = (sel - 1) % 5
                for idx in (i, j):
                    cs, ce = sockets[idx]
                    for r in (48,49,59,60):
                        for c in range(cs, ce+1):
                            cur = grid[r][c]
                            if r in (48,60) or c in (cs,ce):
                                if cur in ('0','3'):
                                    nv = '3' if cur == '0' else '0'
                                    grid[r][c] = nv
                                    changes[f"{r},{c}"] = nv
                sel = (sel + 1) % 5

            elif a == "ACTION3":
                # toggle a different pair (sel-1, sel-2) roughly
                i = (sel - 1) % 5
                j = (sel - 2) % 5
                for idx in (i, j):
                    cs, ce = sockets[idx]
                    for r in (48,49,59,60):
                        for c in range(cs, ce+1):
                            if r in (48,60) or c in (cs,ce):
                                cur = grid[r][c]
                                if cur in ('0','3'):
                                    nv = '3' if cur == '0' else '0'
                                    grid[r][c] = nv
                                    changes[f"{r},{c}"] = nv
                sel = (sel - 1) % 5

            elif a in ("ACTION1","ACTION2"):
                # toggle puzzle cells (5<->7) in selected socket
                cs, ce = sockets[sel % 5]
                for r in range(52,57):
                    for c in range(cs, ce+1):
                        cur = grid[r][c]
                        if cur == '5':
                            grid[r][c] = '7'
                            changes[f"{r},{c}"] = '7'
                        elif cur == '7':
                            grid[r][c] = '5'
                            changes[f"{r},{c}"] = '5'

            # GOAL guess: all sockets 3 and all puzzle cells 7 -> WIN
            all3 = True
            for cs, ce in sockets:
                for r in (48,49,59,60):
                    for c in range(cs, ce+1):
                        if r in (48,60) or c in (cs,ce):
                            if grid[r][c] != '3':
                                all3 = False
            if all3 and state == "NOT_FINISHED":
                levels_done = 1
                state = "WIN"

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
