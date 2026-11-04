def predict(probe):
    # Beliefs (from the evidence):
    # - The screen is a 64x64 grid; most cells are static "wall" colour 5.
    # - There is a visible "counter" drawn at r63: a run of 5s at the bottom-right
    #   that grows leftward by one cell per successful click [E1,E2,E3,E4,E6].
    #   Each click that "counts" sets r63,c = 5 for the next free column c (63,62,...).
    # - Clicks on some objects do nothing (no change) [E1 ACTION2, E2 first click,
    #   E3 first two clicks, E4 third click, E5 ACTION5].
    # - Clicking the "switch" objects toggles a 12x7 block at r25-31,c26-37 between
    #   f and 0, and toggles the small block r7 between 0/3 and 3/0 [E1,E3,E5,E6].
    #   The toggle is the same 95-cell change each time (plus the counter cell).
    # - ACTION1..5 appear to do nothing visible [E1 ACTION2, E5 ACTION5].
    # - The counter increments only on clicks that are "accepted"; accepted clicks
    #   are the ones on the switch objects (the ones producing the 95-cell toggle)
    #   and on certain other objects.
    #
    # Goal guess (?): the level completes when the bottom-right counter fills /
    # reaches a threshold, i.e. after enough accepted clicks. We model the counter
    # growing; we predict WIN when the counter would reach column 0 (64 accepted
    # clicks) as a placeholder. The real threshold is unknown.

    import copy

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    # Reconstruct mutable grid from frame
    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    # Determine counter position: rightmost run of 5s in row 63 starting from c63.
    # Count how many trailing columns (from 63 leftward) are '5' *and* were set by
    # the counter. We can't distinguish 5-wall from counter 5 directly, so use
    # history to count accepted clicks.
    #
    # Accepted-click count from history: we replay history to know counter length.
    # But we can also just look: the counter cells are 5 and to the right of them
    # the row is 5 too (wall). So we track via history replay.

    def replay_accepts(hist):
        # We approximate: an accepted click is one that, in our model, produces
        # a counter increment. From evidence, clicks on switch objects and on the
        # "counter" objects (8 5, 43 7, 32 39, 40 4, 8 10, etc.) increment.
        # Non-incrementing: ACTIONs, and clicks on 16 16, 32 25, 30 63, 43 4(no),
        # 37 4(toggle), 41 4(toggle).
        # We'll treat clicks as accepted unless they are ACTIONs or known no-ops.
        n = 0
        for a in hist:
            if a.startswith("CLICK"):
                parts = a.split()
                try:
                    x = int(parts[1]); y = int(parts[2])
                except Exception:
                    continue
                if is_switch(x, y):
                    n += 1  # switch also increments counter [E1,E3,E5,E6]
                elif is_noop(x, y):
                    pass
                else:
                    n += 1
            # ACTIONs: no increment
        return n

    def is_switch(x, y):
        # switch objects: 37 4, 41 4, 43 4 (sometimes). From E1 43 4 toggled,
        # E3 43 4 toggled, E5 37 4 toggled, E6 41 4 toggled.
        return (x, y) in [(37, 4), (41, 4), (43, 4)]

    def is_noop(x, y):
        # no-op clicks observed: 16 16, 32 25, 30 63, 43 4 (in E1 first? no,
        # E1 first 43 4 changed 1 cell = counter). Actually 43 4 in E1 changed
        # only counter (1 cell) -> accepted counter click, not toggle.
        # 8 5 sometimes no-op (E2 first, E3 last, E4 third). Hmm inconsistent.
        # We'll treat 16 16, 32 25, 30 63 as no-ops.
        return (x, y) in [(16, 16), (32, 25), (30, 63)]

    counter = replay_accepts(history)

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for a in actions:
        changes = {}
        if a.startswith("CLICK"):
            parts = a.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                steps.append({"changes": {}, "levels": levels_done, "state": state})
                continue

            if is_switch(x, y):
                # toggle 95-cell block
                # r7 c35-39 and c41-45 swap between (0,3) and (3,0)
                # r25-31 c26-37 swap between f and 0
                # Determine current state from grid
                cur7 = grid[7][35]
                new7a = '3' if cur7 == '0' else '0'
                new7b = '0' if cur7 == '0' else '3'
                for c in range(35, 40):
                    if grid[7][c] != new7a:
                        grid[7][c] = new7a
                        changes["7,%d" % c] = new7a
                for c in range(41, 46):
                    if grid[7][c] != new7b:
                        grid[7][c] = new7b
                        changes["7,%d" % c] = new7b
                curf = grid[25][26]
                newf = '0' if curf == 'f' else 'f'
                for r in range(25, 32):
                    for c in range(26, 38):
                        if grid[r][c] != newf:
                            grid[r][c] = newf
                            changes["%d,%d" % (r, c)] = newf
                # counter increment
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
            elif is_noop(x, y):
                pass
            else:
                # accepted counter click
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
        else:
            # ACTIONs: no change
            pass

        if counter >= 64:
            state = "WIN"
            levels_done = 1

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
