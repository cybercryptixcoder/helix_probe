def predict(probe):
    # Beliefs:
    # - Bottom row r63 is a move-counter: effective CLICKs fill cells from c63 leftward.
    #   Counter position = number of effective clicks so far (from history). [E1-E29]
    # - When counter reaches c0 and another effective click lands, GAME_OVER. [E29]
    # - CLICK 43 4 / 37 4 / 41 4 toggle r7 c35-45 pattern (0<->3 swap) and
    #   redraw a rectangle rows 25-31/33-44 cols 26-37/39-45 between 0 and f. [E1,E3,E5,E13,E14,E15,E17,E25,E35,E41]
    # - CLICK 43 7 toggles similarly (r7 c35-45) plus r33-44 block. [E4,E43]
    # - ACTION1-5 redraw a creature sprite region (rows 21-56). Complex; approximate. [E7,E8,E10,E12,E19,E21,E26]
    # - Many CLICKs do nothing (already-used spots / non-reactive). [E2,E11,E16,...]
    # - RESET restores level. [E30]
    # - GOAL (?): fill the counter to c0 without triggering GAME_OVER, or complete
    #   a puzzle using the toggles. Best guess: reaching c0 exactly = win is WRONG (E29 = GAME_OVER).
    #   Likely goal: toggle regions to a target pattern. Marked "?" - unproven.

    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])
    level = probe.get("level", 0)

    # Parse frame into grid
    grid = [list(row) for row in frame] if frame else [['5']*64 for _ in range(64)]

    # Reconstruct counter position from history: count effective clicks.
    # We approximate: each CLICK that isn't a known toggle-region click advances counter.
    # Toggle clicks (43 4, 37 4, 41 4, 43 7) do NOT advance counter (they toggle).
    toggle_spots = {(43,4),(37,4),(41,4),(43,7)}
    counter = 0
    for a in history:
        if a.startswith("CLICK"):
            try:
                _, x, y = a.split()
                x, y = int(x), int(y)
            except:
                continue
            if (x,y) in toggle_spots:
                continue
            # unknown clicks: assume effective if not obviously no-op; count them
            counter += 1
        # ACTIONs don't advance counter
    # clamp
    counter = min(counter, 64)

    steps = []
    for a in actions:
        changes = {}
        state = "NOT_FINISHED"
        levels = 0
        if a == "RESET":
            # restore - we can't know exact; emit no changes (approximation)
            counter = 0
        elif a.startswith("CLICK"):
            try:
                _, x, y = a.split()
                x, y = int(x), int(y)
            except:
                x, y = -1, -1
            if (x,y) in toggle_spots:
                # toggle r7 c35-45: swap 0<->3
                for c in range(35,46):
                    old = grid[7][c]
                    new = '3' if old=='0' else ('0' if old=='3' else old)
                    if new != old:
                        changes[f"7,{c}"] = new
                        grid[7][c] = new
                # toggle a block rows 25-31 cols 26-37 (0<->f) - approximate
                for r in range(25,32):
                    for c in range(26,38):
                        old = grid[r][c]
                        new = 'f' if old=='0' else ('0' if old=='f' else old)
                        if new != old:
                            changes[f"{r},{c}"] = new
                            grid[r][c] = new
            else:
                # advance counter
                if counter < 64:
                    col = 63 - counter
                    if col >= 0:
                        if grid[63][col] != '5':
                            changes[f"63,{col}"] = '5'
                            grid[63][col] = '5'
                        counter += 1
                        if counter >= 64:
                            state = "GAME_OVER"
                else:
                    state = "GAME_OVER"
        elif a.startswith("ACTION"):
            # sprite redraw - approximate: no precise prediction
            pass
        steps.append({"changes": changes, "levels": levels, "state": state})
    return {"steps": steps}
