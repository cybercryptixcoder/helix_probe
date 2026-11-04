def predict(probe):
    # Beliefs (from evidence):
    # - Grid 64x64; colour 5 is background/wall.
    # - Row 63 is a "cursor" that paints cells 5 moving leftward, one per accepted click.
    #   Cursor col = 63 - (number of accepted clicks since level start) [E1-E10].
    # - Accepted clicks: most CLICKs on objects advance the cursor by 1.
    #   Inert clicks (no change): 16 16 [E1], 32 25 [E3], 8 5 sometimes [E2,E3,E4].
    #   Treat 8 5 as inert (E2 first, E3 last, E4 all showed 0 change) -> inert.
    # - Switch objects (37 4, 41 4, 43 4) toggle a 95-cell block AND advance cursor.
    #   Toggle: r7 c35-39 and c41-45 swap 0<->3; r25-31 c26-37 swap f<->0.
    # - ACTION1..5 each paint a distinct sprite in region ~r21-52, c25-49 [E7,E8,E9,E10].
    #   These are animation frames; each ACTION sets a specific sprite pattern.
    #   We approximate: ACTION2 paints a "2"-outline sprite [E10], ACTION3 paints 5-blob [E8],
    #   ACTION4 paints f-blob [E9], ACTION5 paints f-blob [E7]. ACTION1 unknown "?".
    #   Since exact patterns are complex, we model each ACTION as painting a canonical sprite.
    # - Cursor count: replay history counting accepted clicks. Cursor col = 63 - count.
    #
    # Goal guess (?): level completes when cursor reaches col 0 (count 64). Threshold unknown.

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    SWITCHES = {(37, 4), (41, 4), (43, 4)}
    INERT = {(16, 16), (32, 25), (8, 5)}

    def is_switch(x, y):
        return (x, y) in SWITCHES

    def is_inert(x, y):
        return (x, y) in INERT

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
        return n

    counter = count_accepts(history)

    # Sprite patterns (approximate canonical forms). Region roughly r21-52, c25-49.
    # Each ACTION paints its own sprite; we set a bounding region to 5 then draw the sprite.
    def sprite_A():  # ACTION5 [E7]: f-blob lower region
        ch = {}
        for r in range(34, 39):
            for c in range(27, 37):
                ch[(r, c)] = 'f'
        return ch

    def sprite_B():  # ACTION4 [E9]: f-blob with 2 outline, upper-right
        ch = {}
        for r in range(21, 35):
            for c in range(25, 50):
                ch[(r, c)] = '5'
        for r in range(24, 35):
            for c in range(25, 38):
                ch[(r, c)] = '5'
        for r in range(24, 35):
            for c in range(38, 50):
                ch[(r, c)] = 'f'
        return ch

    def sprite_C():  # ACTION3 [E8]: 5-blob with 2/f
        ch = {}
        for r in range(21, 39):
            for c in range(25, 50):
                ch[(r, c)] = '5'
        for r in range(24, 35):
            for c in range(25, 38):
                ch[(r, c)] = '2'
        for r in range(25, 32):
            for c in range(26, 37):
                ch[(r, c)] = 'f'
        return ch

    def sprite_D():  # ACTION2 [E10]: 2-outline blob
        ch = {}
        for r in range(21, 46):
            for c in range(25, 50):
                ch[(r, c)] = '5'
        for r in range(32, 46):
            for c in range(38, 47):
                ch[(r, c)] = '2'
        for r in range(33, 45):
            for c in range(39, 46):
                ch[(r, c)] = 'f'
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
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
            else:
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
        elif a == "ACTION5":
            target = sprite_A()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        elif a == "ACTION4":
            target = sprite_B()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        elif a == "ACTION3":
            target = sprite_C()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        elif a == "ACTION2":
            target = sprite_D()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        elif a == "ACTION1":
            # "?" unknown; guess it paints sprite_C-like
            target = sprite_C()
            for (r, c), v in target.items():
                if grid[r][c] != v:
                    grid[r][c] = v
                    changes["%d,%d" % (r, c)] = v
        else:
            pass

        if counter >= 64:
            state = "WIN"
            levels_done = 1

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
