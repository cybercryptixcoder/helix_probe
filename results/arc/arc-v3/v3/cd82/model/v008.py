def predict(probe):
    # Beliefs (from evidence):
    # - Grid 64x64; colour 5 is background/wall.
    # - Row 63 has a "cursor" that paints cells 5 moving leftward, one per accepted click.
    #   The cursor position is determined by the number of accepted clicks since level start,
    #   NOT by the visible frame (frame can't distinguish counter-5 from wall-5) [E1-E9].
    # - Accepted clicks: most CLICKs on objects advance the cursor by 1 [E1,E2,E3,E4,E5,E6,E8,E9].
    #   Some clicks are inert (no change at all): 16 16 [E1], 32 25 [E3], 8 5 sometimes [E2,E3,E4].
    #   Inertness of 8 5 is inconsistent -> treat as accepted (majority) but note "?".
    # - Switch objects (37 4, 41 4, 43 4) toggle a 95-cell block AND advance cursor [E1,E3,E5,E6].
    #   Toggle: r7 c35-39 and c41-45 swap 0<->3; r25-31 c26-37 swap f<->0.
    # - ACTION1..5 do nothing visible [E1 ACTION2, E5 ACTION5]. BUT E7/E8/E9 show ACTION4/ACTION5
    #   DO change a large sprite region (r21-38, c25-49) — this contradicts "actions do nothing".
    #   So ACTION4 and ACTION5 toggle a big sprite; ACTION1/ACTION3 also change it [E8].
    #   The sprite region is r21-38, c25-49 roughly; it toggles between two states.
    #   E7 ACTION5: paints f-blob + 2-outline. E8 ACTION3: paints 5-blob + 2/f. E9 ACTION4: paints f-blob.
    #   These are sprite animations; model as toggling a fixed region between two colourings.
    # - Cursor count: replay history counting accepted clicks. Cursor col = 63 - count.
    #   E9: after 25 actions, CLICK 32 36 painted c47 -> count was 16 before, so 63-16=47. Good.
    #   So accepted-click count = (63 - painted_col). We count from history.
    #
    # Goal guess (?): level completes when cursor reaches some threshold (unknown).
    #   Placeholder: WIN when cursor count reaches 64 (col 0). Real threshold unknown.

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    SWITCHES = {(37, 4), (41, 4), (43, 4)}
    INERT = {(16, 16), (32, 25)}

    def is_switch(x, y):
        return (x, y) in SWITCHES

    def is_inert(x, y):
        return (x, y) in INERT

    # Count accepted clicks from history (cursor position).
    def count_accepts(hist):
        n = 0
        for a in hist:
            if a.startswith("CLICK"):
                parts = a.split()
                try:
                    x = int(parts[1]); y = int(parts[2])
                except Exception:
                    continue
                if is_inert(x, y):
                    continue
                n += 1
            # ACTIONs: no cursor change
        return n

    counter = count_accepts(history)

    # Sprite region for ACTION animations: rows 21-38, cols 25-49.
    # Two states: "A" (f-blob with 2 outline, as in E7/E9) and "B" (5-blob, as in E8).
    # We model ACTION4/ACTION5 as setting state A, ACTION1/ACTION3 as setting state B? 
    # Actually E7 ACTION5 -> A, E8 ACTION3 -> B, E9 ACTION4 -> A. ACTION1 in E8 did cursor only.
    # Simplest: each ACTION toggles the sprite region between A and B. "?" uncertain.
    # We'll just toggle: if region currently looks like A, go to B, else A.
    # But we don't have exact pixel data for both states; approximate by toggling f<->5 in region.
    # Given uncertainty, model ACTION4/5 as painting A (f-blob) and ACTION1/3 as painting B (5-blob).
    # This is a guess "?".

    def sprite_state_A():
        # E7/E9 pattern: f-blob with 2 outline
        ch = {}
        # outline (2s) roughly: we set region to a canonical A pattern
        # Since exact pattern is complex, we approximate: set region to '2' border + 'f' fill
        # This won't match exactly but captures that region changes.
        for r in range(21, 39):
            for c in range(25, 50):
                ch[(r, c)] = '2'
        # fill f-blob (approx)
        for r in range(24, 35):
            for c in range(26, 48):
                ch[(r, c)] = 'f'
        return ch

    def sprite_state_B():
        ch = {}
        for r in range(21, 39):
            for c in range(25, 50):
                ch[(r, c)] = '5'
        for r in range(24, 35):
            for c in range(26, 48):
                ch[(r, c)] = '2'
        return ch

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

            if is_inert(x, y):
                pass
            elif is_switch(x, y):
                # toggle 95-cell block
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
                # cursor
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
            else:
                # accepted cursor click
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
        elif a in ("ACTION4", "ACTION5"):
            # paint sprite state A
            target = sprite_state_A()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        elif a in ("ACTION1", "ACTION3"):
            # paint sprite state B "?"
            target = sprite_state_B()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        else:
            # ACTION2: no change
            pass

        if counter >= 64:
            state = "WIN"
            levels_done = 1

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
