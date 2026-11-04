def predict(probe):
    # Beliefs (with evidence):
    # - Row 63 is a timer bar: '4' = empty, '5' = filled, fills right-to-left [E64]
    # - When the bar becomes fully filled (c0 fills last) state = GAME_OVER [E29, E64]
    # - RESET clears the bar back to empty ('4') and returns NOT_FINISHED [E30, E65, E66, E70]
    # - Not every action advances the bar: some actions are "inert" for the bar
    #   (a CLICK that hits nothing new, or a repeated ACTION whose sprite is already drawn)
    #   [E68: 2nd ACTION2 no bar change; E71: CLICK 32 28 no change; E73: ACTION1 no change;
    #    E74: 2nd ACTION1 no change; E75: CLICK 32 39 no change; E76: 3rd ACTION1 no change;
    #    E80: 1st CLICK 16 16 no change; E82: 1st ACTION2 no change]
    # - A CLICK advances the bar only if it hits a "fresh" object/cell not yet used this level;
    #   repeated clicks on the same target become inert [E2,E6,E38,E44,E60,E80]
    # - ACTIONs draw/move a sprite; the bar advances only when the sprite actually changes
    #   (first use of an ACTION after a state change advances; immediate repeat does not)
    #   [E68,E74,E76,E82]
    # - CLICK 43 4 / CLICK 37 4 toggle r7 c35-45 between pattern A and B [E1,E3,...]
    # - Goal guess "?": fill the bar to c0 without... no evidence of WIN; likely GAME_OVER.
    #   No experiment reached levels>=1, so predict no level completion.

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

    # Track memory: last action that advanced the bar / sprite state
    # We model "inert" as: an action is inert if it repeats the immediately-preceding
    # action of the same kind without an intervening state change (best guess).
    # Simpler heuristic matching evidence: an ACTION is inert if it equals the
    # previous action in the sequence (immediate repeat). A CLICK is inert if it
    # targets a cell/object already clicked since the last RESET (we approximate
    # by: same click coordinate seen earlier in history or this probe).
    clicked = set()
    # seed clicked from history (approximate: all CLICK coords in history)
    for h in history:
        h = h.strip()
        if h.startswith("CLICK"):
            p = h.split()
            if len(p) >= 3:
                try:
                    clicked.add((int(p[1]), int(p[2])))
                except Exception:
                    pass

    prev_act = None
    # last action in history
    if history:
        prev_act = history[-1].strip()

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
                clicked = set()
                prev_act = None
            steps.append({"changes": changes, "levels": levels, "state": state})
            continue

        if act == "RESET":
            clear_bar(grid, changes)
            state = "NOT_FINISHED"
            clicked = set()
            prev_act = None
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
            # inert if this coordinate was already clicked
            if (x, y) in clicked:
                inert = True
            else:
                clicked.add((x, y))
        else:
            # ACTION: inert if it immediately repeats the previous action
            if prev_act == act:
                inert = True

        if not inert:
            advance(grid, changes)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"

        prev_act = act
        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
