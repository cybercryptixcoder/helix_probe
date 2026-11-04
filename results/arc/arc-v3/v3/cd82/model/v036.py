def predict(probe):
    # Beliefs:
    # - Row 63 is a progress bar filled left-to-right with '5' as actions are taken [E1,E2,E4,...]
    # - The bar starts empty (all background) at level start / after RESET [E30,E66,E70]
    # - Most actions advance the bar by one cell; the bar fills from c0 rightward [E63,E64]
    # - When the bar is full (c0..c63 all '5'), the next action => GAME_OVER [E64]
    # - RESET restores the level to its initial screen (bar cleared, sprite reset) [E30,E66,E70]
    # - CLICK on certain objects toggles the big f/0 block region (rows ~25-31, cols ~26-37)
    #   AND advances the bar [E1,E13,E17]; but many clicks are inert (no visible change, no advance)
    # - ACTION4 moves the '2/f' sprite AND advances the bar [E69]
    # - ACTION1/2/3/5 sometimes advance the bar, sometimes are inert [E73,E74,E68]
    # - Level completion: UNKNOWN ("?") - not observed. Guess: filling the bar without
    #   overflowing (reaching exactly c63) may complete the level; or clicking a specific
    #   object. Marked "?".
    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    grid = [list(r) for r in frame] if frame else [['5']*64 for _ in range(64)]

    # Count how many bar cells are filled on row 63 (from c0 rightward) in current frame
    def bar_count(g):
        n = 0
        for c in range(64):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    filled = bar_count(grid)

    steps = []
    state = "NOT_FINISHED"
    levels = 0

    # We treat each action as advancing the bar by 1 (best guess), except RESET.
    # CLICK on known toggle objects also toggles the f/0 block.
    toggle_objs = {(37,4),(41,4),(43,4)}

    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            steps.append({"changes": {}, "levels": levels, "state": state})
            continue
        if a == "RESET":
            # restart: bar cleared, sprite reset. We approximate by clearing row 63.
            for c in range(64):
                if grid[63][c] != '5':
                    grid[63][c] = '5'
                    changes["63,%d" % c] = '5'
            filled = 0
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        # advance bar
        if filled < 64:
            grid[63][filled] = '5'
            changes["63,%d" % filled] = '5'
            filled += 1
        else:
            state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        # toggle region for known toggle objects
        if a.startswith("CLICK"):
            try:
                parts = a.split()
                x, y = int(parts[1]), int(parts[2])
            except Exception:
                x = y = -1
            if (x, y) in toggle_objs:
                for r in range(25, 32):
                    for c in range(26, 38):
                        cur = grid[r][c]
                        new = '0' if cur == 'f' else 'f'
                        grid[r][c] = new
                        changes["%d,%d" % (r, c)] = new
        steps.append({"changes": changes, "levels": levels, "state": state})
    return {"steps": steps}
