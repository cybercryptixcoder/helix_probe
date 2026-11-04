def predict(probe):
    # Beliefs (revised):
    # - Row 63 is a counter/bar. It fills from the RIGHT (c63) leftward with '5' as actions are taken [E64,E66,E67,E68,E70,E71,E72,E74,E76].
    #   (Earlier "left-to-right from c0" was wrong: observed fills are at c63,c62,c61,...)
    # - The bar starts EMPTY at level start / after RESET (all background, no '5' cells) [E30,E66,E70].
    # - Each accepted action paints the next cell leftward: c63, then c62, ... [E74: c60,c59,c58; E76: c57,c56].
    # - Some actions are inert (no bar advance): ACTION1 sometimes no-op [E73,E74,E76]; CLICK on some objects no-op [E67,E71,E72,E75].
    #   Inertness is not fully predictable from visible state; model as: ACTION1/ACTION2 sometimes inert.
    # - When bar is full (c0..c63 all '5'), next action => GAME_OVER [E64].
    # - RESET restores level to initial screen (bar cleared, sprite reset) [E30,E66,E70].
    # - ACTION4 moves the '2/f' sprite [E69]; ACTION2/3/5 may move sprite too.
    # - CLICK on certain objects toggles the big f/0 block region (rows ~25-31, cols ~26-37) [E1,E13,E17].
    # - Level completion: UNKNOWN ("?"). Guess: filling the bar exactly (reaching c0) then one more action
    #   may complete the level, OR clicking a specific object. Marked "?".
    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    grid = [list(r) for r in frame] if frame else [['5']*64 for _ in range(64)]

    # Count filled bar cells on row 63. Bar fills from RIGHT (c63) leftward.
    # Count contiguous '5' run starting at c63 going left.
    def bar_count(g):
        n = 0
        for c in range(63, -1, -1):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    filled = bar_count(grid)

    steps = []
    state = "NOT_FINISHED"
    levels = 0

    toggle_objs = {(37,4),(41,4),(43,4)}

    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            steps.append({"changes": {}, "levels": levels, "state": state})
            continue
        if a == "RESET":
            for c in range(64):
                if grid[63][c] != '5':
                    grid[63][c] = '5'
                    changes["63,%d" % c] = '5'
            filled = 0
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        # Determine if this action advances the bar (best guess).
        # ACTION1/ACTION2 sometimes inert; CLICK sometimes inert. We guess most advance.
        advance = True
        if a in ("ACTION1", "ACTION2"):
            # guess: advances unless it's a repeat no-op; approximate as advancing
            advance = True

        if advance:
            if filled < 64:
                col = 63 - filled
                grid[63][col] = '5'
                changes["63,%d" % col] = '5'
                filled += 1
            else:
                state = "GAME_OVER"
                steps.append({"changes": changes, "levels": levels, "state": state})
                continue

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
