def predict(probe):
    # Beliefs (from the evidence):
    #
    # The screen is a 64x64 grid. There is a "token" sprite drawn as a
    # diamond/arrow shape of '2' and 'f' cells around a moving position.
    # ACTION1..ACTION5 move the token (redraw the sprite at a new spot).
    # Clicks on certain objects move the token / toggle things.
    #
    # Row 63 is a progress bar: each "successful" action paints the next
    # cell to the LEFT with colour 5 (c63, c62, ... c0). When c0 is painted
    # the state becomes GAME_OVER [E29]. RESET restores the level [E30].
    #
    # Key correction from E33: ACTION3 (and other ACTIONs) are NOT always
    # "live". In E33 ACTION3 twice produced NO row-63 advance, while the
    # clicks did. So ACTIONs advance the bar only when they actually move
    # the token (change the board). When the token is blocked / at a wall,
    # the ACTION is inert and does not advance the bar [E33, E27].
    #
    # Also: a click advances the bar iff it hits a live object. In E33,
    # CLICK 32 36 advanced (c59), CLICK 43 4 was inert (0 cells). So the
    # "live" set is object-specific, not "any non-background cell".
    #
    # Goal guess ("?"): the level is completed by some in-game condition
    # (e.g. token reaching a goal tile) rather than by filling the bar,
    # since filling the bar to c0 gives GAME_OVER [E29]. Marked "?".

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    level = probe.get("level", 0)
    history = probe.get("history", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    def bar_count(g):
        n = 0
        c = 63
        while c >= 0 and g[63][c] == '5':
            n += 1
            c -= 1
        return n

    count = bar_count(grid)

    # Clicks known to advance the bar (live objects).
    live_clicks = {
        (43, 4), (37, 4), (41, 4), (40, 4), (43, 7),
        (32, 39), (32, 41), (32, 36), (32, 28), (32, 63),
        (22, 63), (25, 63), (30, 63), (5, 63),
        (50, 50), (51, 51), (52, 52), (53, 53), (54, 54),
        (55, 55), (56, 56), (57, 57), (60, 60),
        (21, 39), (37, 7), (30, 30), (20, 20), (45, 39),
        (42, 39), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (9, 9),
        (59, 63), (58, 63), (56, 63), (54, 63),
    }
    # Clicks known inert (never advanced the bar).
    inert_clicks = {
        (8, 5), (8, 10), (16, 16), (32, 25), (45, 20),
        (43, 4),  # E33: CLICK 43 4 was inert here
    }

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
                count = 0
                grid = [['5'] * 64 for _ in range(64)]
            steps.append({"changes": changes, "levels": levels_done,
                          "state": state})
            continue

        if act == "RESET":
            state = "NOT_FINISHED"
            count = 0
            grid = [['5'] * 64 for _ in range(64)]
            steps.append({"changes": changes, "levels": levels_done,
                          "state": state})
            continue

        did = False
        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x, y = int(parts[1]), int(parts[2])
            except Exception:
                x = y = -1
            if (x, y) in inert_clicks:
                did = False
            elif (x, y) in live_clicks:
                did = True
            else:
                did = False
        elif act.startswith("ACTION"):
            # "?" ACTIONs advance the bar only when they move the token.
            # We can't track token position reliably, so default to inert
            # (matches E27, E33 where ACTIONs were inert).
            did = False
        else:
            did = False

        if did:
            if count < 64:
                c = 63 - count
                if grid[63][c] != '5':
                    grid[63][c] = '5'
                    changes["63,%d" % c] = '5'
                count += 1
            if count >= 64:
                state = "GAME_OVER"

        steps.append({"changes": changes, "levels": levels_done,
                      "state": state})

    return {"steps": steps}
