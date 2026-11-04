def predict(probe):
    # Beliefs (from the evidence):
    #
    # Big picture: the screen is a 64x64 grid. There is a "player/token" that
    # is drawn as a small shape around a moving position. Clicks on certain
    # objects move the token / toggle things. The bottom row (r63) is a
    # progress bar: each "successful" click advances a counter and paints one
    # more cell of row 63 from the right edge leftward (c63, c62, ... c0).
    # When the counter reaches 64 (c0 painted) the game is GAME_OVER [E29].
    #
    # Row 63 progress bar:
    #   - Each successful action paints the next cell to the LEFT with colour 5.
    #     First success: r63 c63=5, then c62, c61, ... [E1,E2,E3,E4,...]
    #   - "Successful" = an action that actually did something (a click that
    #     hit a live object, or an ACTION that moved the token / changed board).
    #     Clicks that hit nothing change 0 cells and do NOT advance the bar
    #     [E2 first click, E11, E16 (some), E20 (some), E22 (some), E24...].
    #   - The bar is monotone: once a cell is painted it stays 5.
    #   - When the bar reaches c0 the state becomes GAME_OVER [E29].
    #   - RESET restores the level to its initial screen (bar reset, token
    #     home) and state NOT_FINISHED [E30].
    #
    # The token / moving object:
    #   - ACTION1..ACTION5 move the token one step in some direction, and the
    #     board around it is redrawn (the 200+ cell "changes" are the token
    #     shape plus its trail/background being repainted). The exact direction
    #     per ACTIONn is inferred from the shifts of the drawn shape.
    #   - Clicks on the token's current cell / nearby objects also move it.
    #
    # Because we cannot fully reconstruct the token geometry from the
    # truncated change lists, the model below focuses on the parts that are
    # solidly evidenced and that matter for reaching the goal:
    #   (a) the row-63 progress bar / GAME_OVER rule,
    #   (b) which clicks are "live" (advance the bar) vs inert,
    #   (c) RESET restoring the level.
    #
    # Goal guess ("?"): completing level 1 means filling the row-63 bar all
    # the way WITHOUT hitting GAME_OVER -- i.e. some target number of
    # successful actions, or reaching a special cell. Given the bar runs the
    # full width (64 cells) and c0 triggers GAME_OVER [E29], the level is
    # most likely completed by a specific in-game condition (e.g. moving the
    # token onto a goal tile) rather than by the bar itself. Marked "?".

    import copy

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    level = probe.get("level", 0)
    history = probe.get("history", [])

    # Reconstruct current grid
    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    # Reconstruct the progress-bar counter from the bottom row.
    # Count trailing 5s from the right that form the bar; the bar is the
    # rightmost run of 5s in row 63 that were painted by progress.
    # Simpler & robust: count how many cells in row 63 are '5' starting
    # from c63 going left until a non-5.
    def bar_count(g):
        n = 0
        c = 63
        while c >= 0 and g[63][c] == '5':
            n += 1
            c -= 1
        return n

    count = bar_count(grid)

    # Live-click coordinates observed in the evidence (objects that advance
    # the bar when clicked). These are the clickable objects listed in the
    # prompt plus ones seen in experiments.
    # "?" -- some listed objects are inert (e.g. 8 5, 8 10, 16 16, 32 25,
    # 32 39 sometimes inert). We treat the set of "live" clicks as those that
    # have ever advanced the bar in the evidence.
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
    # Known-inert clicks (never advanced the bar)
    inert_clicks = {
        (8, 5), (8, 10), (16, 16), (32, 25), (45, 20),
    }

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            # Only RESET works
            if act == "RESET":
                state = "NOT_FINISHED"
                count = 0
                grid = [['5'] * 64 for _ in range(64)]
                # "?" exact reset screen unknown here; report no changes
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
                # Unknown click: assume inert unless it's on a non-background
                # coloured cell (heuristic "?").
                did = False
                if 0 <= y < 64 and 0 <= x < 64:
                    if grid[y][x] not in ('5',):
                        did = True
        elif act.startswith("ACTION"):
            # ACTIONs move the token and are generally "live" when they
            # change the board; the evidence shows ACTION1/2/3/4/5 all
            # produced big redraws at least once, but repeated ACTION1 with
            # no change was inert [E27]. We treat ACTION as live "?".
            did = True
        else:
            did = False

        if did:
            # Advance progress bar by one, painting next cell from the right.
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
