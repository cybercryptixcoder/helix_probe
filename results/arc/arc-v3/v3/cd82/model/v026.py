def predict(probe):
    # Beliefs (from the evidence):
    #
    # Row 63 is a progress bar. Each accepted action paints the next cell to
    # the LEFT with colour 5 (c63, c62, ...). When c0 gets painted the state
    # becomes GAME_OVER [E29].
    #
    # An action is "accepted" (advances the bar by exactly 1) iff it visibly
    # changes the board — either it moves a sprite or it hits a live object.
    # Inert actions do NOT advance the bar.
    #   - CLICKs: live objects advance the bar by 1 the FIRST time; a second
    #     click on the same object is inert [E28, E38, E39]. So each object is
    #     a one-shot button.
    #   - ACTIONs: ACTION1/2/4/5 move the '2/f' sprite or the big f-block and
    #     advance the bar when they move something [E34, E36, E40, E42 step1].
    #     But an ACTION can be INERT when the sprite is blocked/occluded and
    #     nothing moves — then the bar does NOT advance [E26/E27 ACTION1 inert;
    #     E42 steps 2 and 4: repeated ACTION1/ACTION2 did not advance the bar].
    #     ACTION3 is inert [E33].  "?" We cannot fully simulate the sprite, so
    #     we approximate: an ACTION advances the bar unless it is a repeat of
    #     the immediately preceding ACTION (sprite already at that position).
    #
    # RESET restores a fresh level-1 screen and clears the bar [E30].
    #
    # Goal guess ("?"): the bar filling to c0 gives GAME_OVER, not a level
    # completion, so completing level 1 is NOT filling the bar. Likely the
    # sprite must reach a goal tile / some puzzle solved. Marked "?".

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

    # Objects known to be live (advance bar once). Everything else inert.
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
    }

    # ACTIONs that can move a sprite (advance bar). ACTION3 is inert.
    live_actions = {"ACTION1", "ACTION2", "ACTION4", "ACTION5"}

    used = set()

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0
    last_action = None

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
                count = 0
                used = set()
                grid = [['5'] * 64 for _ in range(64)]
                last_action = None
            steps.append({"changes": changes, "levels": levels_done,
                          "state": state})
            continue

        if act == "RESET":
            state = "NOT_FINISHED"
            count = 0
            used = set()
            grid = [['5'] * 64 for _ in range(64)]
            last_action = None
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
            if key in live_objects and key not in used:
                did = True
                used.add(key)
        elif act in live_actions:
            # "?" A repeated ACTION is assumed blocked (sprite already moved).
            if act != last_action:
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

        last_action = act
        steps.append({"changes": changes, "levels": levels_done,
                      "state": state})

    return {"steps": steps}
