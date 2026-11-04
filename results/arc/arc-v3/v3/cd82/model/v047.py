def predict(probe):
    # Beliefs (revised v47):
    # - Row 63 is a progress bar filling right-to-left from c63; each accepted action fills one cell.
    # - CLICK: the FIRST click on a given (x,y) cell in the level is inert; every SUBSEQUENT click on that
    #   cell advances the bar by one [E80 N,Y; E48 N,Y; E84 N,Y,~; E86 N,Y,Y; E90; E97; E98 N,Y,N].
    #   E98: CLICK 43 4 x3 -> adv,no,adv: so it's NOT "first inert then all advance". It's the SAME
    #   alternating pattern as ACTION: advance on odd-numbered occurrence within a run of the same click cell.
    #   E84: CLICK 22 48 x3 -> no,adv,no. Hmm that's even,odd,even. Different phase.
    #   E86: CLICK 43 7 x3 -> adv,no,adv (odd). E48: CLICK 55 55 x2 -> adv,no. E98: adv,no,adv.
    #   E84 no,adv,no is the outlier (maybe first click hit something). 
    #   Best unified rule: track consecutive identical actions (same ACTION or same CLICK cell).
    #   Advance when the run length is ODD. This fits E86,E98,E48,E90,E94,E96.
    #   E88 A1,A1,A2,A2 -> adv,no,adv,adv: last A2 is 2nd in run -> even -> no, but observed adv. Outlier.
    #   E84 CLICK22,48 x3 -> no,adv,no: run lengths 1,2,3 -> odd,even,odd -> adv,no,adv, but observed no,adv,no.
    #   E84 is an outlier; accept.
    # - RESET clears row 63 back to '4' [E30,E66,E70,E92,E94,E96]
    # - When bar is full (64 cells) -> GAME_OVER [E30]
    # - GOAL "?": completing level 1 is NOT filling the bar (that gives GAME_OVER). Likely requires
    #   arranging the r7 switch/objects; unproven. Marked "?" below.
    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)
    history = probe.get("history", []) or []
    grid = [list(row) for row in frame] if frame else [['5']*64 for _ in range(64)]

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
                key = ("C", int(p[1]), int(p[2]))
            except Exception:
                key = ("C", -1, -1)
        else:
            key = ("A", act)

        if key == run_key:
            run_len += 1
        else:
            run_key = key
            run_len = 1

        # advance on odd-numbered occurrence within a run
        if run_len % 2 == 1:
            advance(grid, ch)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"
        steps.append({"changes": ch, "levels": levels, "state": state})
    return {"steps": steps}
