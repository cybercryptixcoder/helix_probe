def predict(probe):
    # Beliefs:
    # Row 63 is a progress bar filled left-to-right from c63 downward as
    # "accepted" actions occur; filling c0 -> GAME_OVER [E29].
    # An action is "accepted" iff it causes a visible board change OR is a
    # first-time click on a live button object [E46, E48].
    # CLICK on a background '5' cell: first click inert, second advances
    # [E48]. CLICK on a fresh live object: advances [E46 16,16].
    # CLICK on a dead fresh object: inert [E46 29,36].
    # ACTION1/2/4/5 move the '2/f' sprite and advance the bar when they move
    # something [E34, E36, E40, E42, E50]. ACTION3 is inert [E33].
    # The sprite moves in a cycle: ACTION1 up-left, ACTION2 down-right,
    # ACTION4 up, ACTION5 down (approx). Repeated ACTIONs still move it
    # (E50: ACTION1 twice both moved the sprite and both advanced bar).
    # RESET restores fresh level-1 screen and clears bar [E30].
    # Goal "?": unknown; filling the bar gives GAME_OVER, not level-up.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
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

    # Live button objects (first click advances bar).
    live_objects = {
        (43, 4), (37, 4), (41, 4), (40, 4), (43, 7),
        (32, 39), (32, 41), (32, 36), (32, 28), (32, 63),
        (22, 63), (25, 63), (30, 63), (5, 63),
        (50, 50), (51, 51), (52, 52), (53, 53), (54, 54),
        (55, 55), (56, 56), (57, 57), (60, 60),
        (21, 39), (37, 7), (30, 30), (20, 20), (45, 39),
        (42, 39), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
        (6, 6), (7, 7), (9, 9),
        (59, 63), (58, 63), (56, 63), (54, 63),
        (33, 40), (16, 16), (17, 63),
    }
    dead_objects = {(29, 36)}

    live_actions = {"ACTION1", "ACTION2", "ACTION4", "ACTION5"}

    used = set()
    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
                count = 0
                used = set()
                grid = [['5'] * 64 for _ in range(64)]
            steps.append({"changes": changes, "levels": levels_done,
                          "state": state})
            continue

        if act == "RESET":
            state = "NOT_FINISHED"
            count = 0
            used = set()
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
            key = (x, y)
            if key in dead_objects:
                did = False
            elif key in live_objects:
                if key not in used:
                    did = True
                    used.add(key)
            else:
                # Unknown cell: background '5' first click inert, second
                # advances [E48]. Treat as live-on-second-click.
                if key in used:
                    did = True
                else:
                    used.add(key)
        elif act in live_actions:
            did = True
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
