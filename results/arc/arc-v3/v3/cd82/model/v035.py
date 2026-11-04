def predict(probe):
    # Beliefs:
    # - Row 63 holds a right-to-left progress counter; starts at c63 [E1,E66,E70]
    # - Most actions advance counter one cell left [E1,E2,E4,...]
    # - CLICK on objects (37/41/43,4) toggles an f/0 region AND advances [E1,E13,E17]
    # - Counter reaching past c0 => GAME_OVER [E29,E64]
    # - RESET restarts level: counter back to c63 [E30,E65,E66,E70]
    # - Level completion: UNKNOWN ("?") - not observed in any experiment.
    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    grid = [list(r) for r in frame] if frame else [['5']*64 for _ in range(64)]

    # reconstruct counter position from history since last RESET
    # counter column = 63 - (number of advancing actions since reset)
    # We approximate: each action advances by 1 (best guess)
    idx = 0
    for a in history:
        if a == "RESET":
            idx = 0
        else:
            idx += 1
    col = 63 - idx

    steps = []
    state = "NOT_FINISHED"
    levels = 0
    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            steps.append({"changes": {}, "levels": levels, "state": state})
            continue
        if a == "RESET":
            # restart: counter to c63; we don't fully model screen reset
            idx = 0
            col = 63
            steps.append({"changes": {}, "levels": levels, "state": state})
            continue
        # advance counter
        col -= 1
        if col >= 0:
            changes["63,%d" % col] = "5"
        else:
            state = "GAME_OVER"
        # toggle region for known toggle objects
        if a.startswith("CLICK"):
            try:
                parts = a.split()
                x, y = int(parts[1]), int(parts[2])
            except Exception:
                x = y = -1
            if (x, y) in [(37,4),(41,4),(43,4)]:
                # toggle the f/0 region rows 25-31 cols 26-37 (approx)
                for r in range(25, 32):
                    for c in range(26, 38):
                        cur = grid[r][c]
                        new = '0' if cur == 'f' else 'f'
                        grid[r][c] = new
                        changes["%d,%d" % (r, c)] = new
        steps.append({"changes": changes, "levels": levels, "state": state})
    return {"steps": steps}
