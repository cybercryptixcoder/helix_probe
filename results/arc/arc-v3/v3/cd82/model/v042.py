def predict(probe):
    # Beliefs (with evidence):
    # - Row 63 is a timer bar: '4'=empty, '5'=filled, fills right-to-left [E64]
    # - Bar fully filled (c0 last) => GAME_OVER [E29,E64]
    # - RESET clears bar to '4', returns NOT_FINISHED [E30,E65,E66,E70]
    # - A CLICK advances the bar iff its target is "fresh" (not clicked since last
    #   sprite-drawing ACTION or RESET) [E2,E6,E38,E44,E60,E80,E83]
    # - A sprite-drawing ACTION clears the clicked set (objects become fresh again)
    #   [E83: CLICK 32 39 advances after E82's ACTION2, though inert at E75] ?
    # - An ACTION advances the bar iff it is not an immediate repeat of the previous
    #   action [E68,E74,E76,E82]
    # - CLICK 43 4 / CLICK 37 4 toggle r7 c35-45 between pattern A and B [E1,E3,...]
    # - Goal guess "?": filling the bar to c0 => GAME_OVER, not WIN. No evidence of
    #   level completion; predict no level completion.

    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)
    history = probe.get("history", []) or []

    grid = [list(row) for row in frame] if frame else [['5'] * 64 for _ in range(64)]

    def bar_fill(g):
        n = 0
        for c in range(63, -1, -1):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    def clear_bar(g, changes):
        for c in range(64):
            if g[63][c] != '4':
                changes[f"63,{c}"] = '4'
                g[63][c] = '4'

    def toggle_r7(g, changes):
        seg = [g[7][c] for c in range(35, 46)]
        isA = (seg[0:5] == ['0'] * 5 and seg[6:11] == ['3'] * 5)
        if isA:
            newA = '3'; newB = '0'
        else:
            newA = '0'; newB = '3'
        for c in range(35, 40):
            if g[7][c] != newA:
                changes[f"7,{c}"] = newA
                g[7][c] = newA
        for c in range(41, 46):
            if g[7][c] != newB:
                changes[f"7,{c}"] = newB
                g[7][c] = newB

    # Replay history to reconstruct clicked set and prev_act.
    clicked = set()
    prev_act = None
    for h in history:
        h = h.strip()
        if h == "RESET":
            clicked = set(); prev_act = None
        elif h.startswith("CLICK"):
            p = h.split()
            try:
                clicked.add((int(p[1]), int(p[2])))
            except Exception:
                pass
            prev_act = h
        elif h.startswith("ACTION"):
            # sprite-drawing ACTION clears freshness
            clicked = set()
            prev_act = h

    steps = []
    state = "NOT_FINISHED"
    levels = level

    def advance(g, changes):
        fill = bar_fill(g)
        if fill < 64:
            col = 63 - fill
            if g[63][col] != '5':
                changes[f"63,{col}"] = '5'
                g[63][col] = '5'
                return True
        return False

    for act in actions:
        changes = {}
        act = act.strip()

        if state == "GAME_OVER":
            if act == "RESET":
                clear_bar(grid, changes)
                state = "NOT_FINISHED"
                clicked = set(); prev_act = None
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        if act == "RESET":
            clear_bar(grid, changes)
            state = "NOT_FINISHED"
            clicked = set(); prev_act = None
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        inert = False

        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                x = y = -1
            if (x, y) in ((43, 4), (37, 4)):
                toggle_r7(grid, changes)
            if (x, y) in clicked:
                inert = True
            else:
                clicked.add((x, y))
        else:
            if prev_act == act:
                inert = True
            else:
                # sprite-drawing ACTION clears freshness
                clicked = set()

        if not inert:
            advance(grid, changes)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"

        prev_act = act
        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
