def predict(probe):
    # Beliefs:
    # - Row 63 is a progress bar filling right-to-left from c63; each "accepted" action fills one more cell [E20,E22,E60,E62]
    # - A CLICK advances the bar on even-numbered clicks of the same cell (counts%2==0); first click is inert [E2,E44,E48,E71,E72,E75,E83,E84]
    # - An ACTION advances the bar when it differs from the previous action [E54,E58,E62,E68]
    # - ACTIONs also draw a moving sprite (2/f) but that's cosmetic for the bar [E81,E82,E85]
    # - CLICK 43 4 / 37 4 does NOT toggle r7 (E85 disproves the old toggle rule)
    # - RESET clears row 63 back to '4' [E30,E66,E70]
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

    # replay history to recover per-cell click counts and previous action
    counts = {}
    prev_act = None
    for h in history:
        h = h.strip()
        if h == "RESET":
            counts = {}
            prev_act = None
        elif h.startswith("CLICK"):
            p = h.split()
            try:
                t = (int(p[1]), int(p[2]))
            except Exception:
                t = None
            if t:
                counts[t] = counts.get(t, 0) + 1
            prev_act = h
        elif h.startswith("ACTION"):
            prev_act = h

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
                counts = {}
                prev_act = None
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue
        if act == "RESET":
            clear_bar(grid, ch)
            state = "NOT_FINISHED"
            counts = {}
            prev_act = None
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue

        if act.startswith("CLICK"):
            p = act.split()
            try:
                x = int(p[1]); y = int(p[2])
            except Exception:
                x = y = -1
            t = (x, y)
            counts[t] = counts.get(t, 0) + 1
            if counts[t] % 2 == 0:
                advance(grid, ch)
        else:
            if prev_act != act:
                advance(grid, ch)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"
        prev_act = act
        steps.append({"changes": ch, "levels": levels, "state": state})
    return {"steps": steps}
