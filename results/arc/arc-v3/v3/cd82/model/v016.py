def predict(probe):
    # Beliefs (from evidence):
    # - Grid 64x64; colour 5 is background.
    # - Row 63 is a cursor that paints cells to 5 moving leftward, one per accepted click.
    #   Cursor col = 63 - (number of accepted clicks since level start) [E2-E22].
    # - Inert clicks (no change, no cursor advance): 16 16 [E1], 32 25 [E3],
    #   8 5 [E2,E3,E4,E13], 8 10 [E11], (1,1),(4,4),(7,7) [E16].
    #   Accepted in E16: (2,2),(3,3),(5,5),(6,6),(9,9).
    # - E20: clicking a row-63 cell already painted '5' is inert (no advance).
    # - E22: clicking a fresh non-row-63 cell advances cursor; clicking one that
    #   was already clicked before (50 50 was clicked in E14) is inert.
    #   So: a click is inert if the target cell is already '5' (background) OR
    #   was previously clicked. Simplification: inert if cell already '5'.
    # - Switch objects (37 4, 41 4, 43 4) toggle blocks AND advance cursor.
    #   Toggle: r7 c35-39 and c41-45 swap 0<->3.
    #   Also toggles vertical 7x7 block f<->0 at r25-31 c26-37 when in original f state;
    #   once overwritten by sprites, toggles r33-44 c39-45 f<->0 [E13,E14,E15,E17].
    # - ACTION1..5 each paint a sprite in region ~r21-56, c14-49 [E7-E21].
    #   ACTIONs do NOT advance the cursor.
    #
    # Goal guess (?): level completes when cursor reaches col 0 (count 64).

    level = probe.get("level", 0)
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])

    if frame is None:
        grid = [['5'] * 64 for _ in range(64)]
    else:
        grid = [list(row) for row in frame]

    SWITCHES = {(37, 4), (41, 4), (43, 4)}
    INERT = {(16, 16), (32, 25), (8, 5), (8, 10), (1, 1), (4, 4), (7, 7)}

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

    def sprite_A():  # ACTION5 [E7]: f-blob lower region
        ch = {}
        for r in range(34, 39):
            for c in range(27, 37):
                ch[(r, c)] = 'f'
        return ch

    def sprite_B():  # ACTION4 [E7,E9,E13]: f-blob with 2 outline, upper-right
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

    def sprite_C():  # ACTION3 [E18,E19]: clear + diagonal 2-outline + 0-fill
        ch = {}
        for r in range(40, 55):
            for c in range(25, 50):
                ch[(r, c)] = '5'
        diag = [
            (40, 20), (41, 19), (41, 20), (42, 18), (42, 19),
            (43, 17), (43, 18), (44, 16), (44, 17), (45, 15), (45, 16),
            (46, 14), (46, 15), (47, 15), (47, 16), (48, 16), (48, 17),
            (49, 17), (49, 18), (50, 18), (50, 19), (51, 19), (51, 20),
            (52, 20), (52, 21), (53, 21), (53, 22), (54, 22), (54, 23),
        ]
        for (r, c) in diag:
            ch[(r, c)] = '2'
        for r in range(45, 54):
            for c in range(25, 38):
                ch[(r, c)] = '2'
        for r in range(46, 53):
            for c in range(26, 37):
                ch[(r, c)] = '0'
        return ch

    def sprite_D():  # ACTION2 [E10,E17]: 2-outline blob
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

    def sprite_E():  # ACTION1 [E12,E21]: 2-outline with 0-fill, lower-left
        ch = {}
        for r in range(32, 57):
            for c in range(14, 50):
                ch[(r, c)] = '5'
        for r in range(32, 45):
            for c in range(17, 26):
                ch[(r, c)] = '2'
        for r in range(33, 44):
            for c in range(18, 25):
                ch[(r, c)] = '0'
        return ch

    def toggle_region(ch, r0, r1, c0, c1, a, b):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                v = grid[r][c]
                if v == a:
                    grid[r][c] = b
                    ch["%d,%d" % (r, c)] = b
                elif v == b:
                    grid[r][c] = a
                    ch["%d,%d" % (r, c)] = a

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
                toggle_region(changes, 25, 31, 26, 37, 'f', '0')
                toggle_region(changes, 33, 44, 39, 45, 'f', '0')
                if counter < 64:
                    col = 63 - counter
                    counter += 1
                    grid[63][col] = '5'
                    changes["63,%d" % col] = '5'
            else:
                # inert if target cell already '5' (background)
                if grid[y][x] == '5':
                    pass
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
            target = sprite_E()
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
