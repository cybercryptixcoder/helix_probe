def predict(probe):
    # Beliefs (revised v48):
    # - Row 63 is a progress bar filling right-to-left from c63; each accepted action fills one cell.
    # - Advance rule: track consecutive identical actions (same ACTION or same CLICK cell).
    #   Advance when the run length is ODD. Fits E86(43 7:no,adv,no? no—outlier),E98(43 4:adv,no,adv),
    #   E48(55 55:adv,no),E90,E94,E96.
    # - EXCEPTION: CLICK 40 4 is INERT — it never advances the bar [E93 no, E97 no, E99 no].
    #   This is a specific dead cell; all other clicks follow the odd-run rule.
    # - RESET clears row 63 back to '4' [E30,E66,E70,E92,E94,E96]
    # - When bar is full (64 cells) -> GAME_OVER [E30]
    # - GOAL "?": completing level 1 is NOT filling the bar (that gives GAME_OVER). Likely requires
    #   arranging the r7 switch/objects; unproven. Marked "?" below.
    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)
    history = probe.get("history", []) or []
    grid = [list(row) for row in frame] if frame else [['5']*64 for _ in range(64)]

    INERT_CLICKS = {(40, 4)}

    def bar_fill(g):
        n = 0
        for c in range(63, -1, -1):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    def clear_bar(g, ch):
        for c in range(64):
            if g[63][c] != '4':
                ch["63,%d" % c] = '4'
                g[63][c] = '4'

    # replay history to recover run state (consecutive identical action key)
    run_key = None
    run_len = 0
    for h in history:
        h = h.strip()
        if h == "RESET":
            run_key = None
            run_len = 0
        elif h.startswith("CLICK"):
            p = h.split()
            try:
                key = ("C", int(p[1]), int(p[2]))
            except Exception:
                key = ("C", -1, -1)
            if key == run_key:
                run_len += 1
            else:
                run_key = key
                run_len = 1
        elif h.startswith("ACTION"):
            key = ("A", h)
            if key == run_key:
                run_len += 1
            else:
                run_key = key
                run_len = 1

    steps = []
    state = "NOT_FINISHED"
    levels = level

    def advance(g, ch):
        fill = bar_fill(g)
        if fill < 64:
            col = 63 - fill
            if g[63][col] != '5':
                ch["63,%d" % col] = '5'
                g[63][col] = '5'
                return True
        return False

    for act in actions:
        ch = {}
        act = act.strip()
        if state == "GAME_OVER":
            if act == "RESET":
                clear_bar(grid, ch)
                state = "NOT_FINISHED"
                run_key = None
                run_len = 0
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue
        if act == "RESET":
            clear_bar(grid, ch)
            state = "NOT_FINISHED"
            run_key = None
            run_len = 0
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue

        if act.startswith("CLICK"):
            p = act.split()
            try:
                cx, cy = int(p[1]), int(p[2])
                key = ("C", cx, cy)
            except Exception:
                cx, cy = -1, -1
                key = ("C", -1, -1)
        else:
            cx, cy = None, None
            key = ("A", act)

        if key == run_key:
            run_len += 1
        else:
            run_key = key
            run_len = 1

        # advance on odd-numbered occurrence within a run, unless the click is on an inert cell
        is_inert = (cx is not None) and ((cx, cy) in INERT_CLICKS)
        if (run_len % 2 == 1) and not is_inert:
            advance(grid, ch)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"
        steps.append({"changes": ch, "levels": levels, "state": state})
    return {"steps": steps}
