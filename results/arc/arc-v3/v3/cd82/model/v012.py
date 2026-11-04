def predict(probe):
    # Beliefs (from evidence):
    # - Grid 64x64; colour 5 is background.
    # - Row 63 is a cursor that paints cells 5 moving leftward, one per accepted click.
    #   Cursor col = 63 - (number of accepted clicks since level start) [E2-E14].
    #   The cursor advances on EVERY click that is not inert, regardless of what it hits.
    # - Inert clicks (no change, no cursor advance): 16 16 [E1], 32 25 [E3],
    #   8 5 [E2,E3,E4,E13], 8 10 [E11]. (8 5 is inert: E2 first showed 0 change.)
    # - Switch objects (37 4, 41 4, 43 4) toggle blocks AND advance cursor.
    #   Toggle: r7 c35-39 and c41-45 swap 0<->3.
    #   Also toggles a vertical 7x7 block of f<->0 at r25-31 c26-37 [E3,E5,E6,E10]
    #   BUT only when that block is still in its original f state; once overwritten
    #   by sprites (E13,E14) the switch only toggles r7 and the sprite region
    #   r33-44 c39-45 f<->0 (E13,E14). Model: switch toggles r7 always, and toggles
    #   whichever of {r25-31 c26-37, r33-44 c39-45} currently holds f/0.
    # - ACTION1..5 each paint a sprite in region ~r21-56, c25-49 [E7-E12].
    #   Sprites overwrite the region; ACTION2 is not inert (paints sprite) [E10].
    # - Cursor count: replay history counting accepted clicks. Cursor col = 63 - count.
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
    INERT = {(16, 16), (32, 25), (8, 5), (8, 10)}

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

    # Sprite patterns (approximate canonical forms). Region roughly r21-56, c25-49.
    def sprite_A():  # ACTION5 [E7]: f-blob lower region
        ch = {}
        for r in range(34, 39):
            for c in range(27, 37):
                ch[(r, c)] = 'f'
        return ch

    def sprite_B():  # ACTION4 [E7,E9]: f-blob with 2 outline, upper-right
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

    def sprite_E():  # ACTION1 [E12]: 2-outline with f-fill, lower region
        ch = {}
        for r in range(32, 57):
            for c in range(33, 50):
                ch[(r, c)] = '5'
        for r in range(32, 45):
            for c in range(38, 47):
                ch[(r, c)] = '2'
        for r in range(33, 45):
            for c in range(39, 46):
                ch[(r, c)] = 'f'
        return ch

    def toggle_region(ch, r0, r1, c0, c1, a, b):
        # toggle cells that are 'a' -> 'b' and 'b' -> 'a'
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
                # r7 toggle
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
                # toggle whichever sprite-region block currently holds f/0
                toggle_region(changes, 25, 31, 26, 37, 'f', '0')
                toggle_region(changes, 33, 44, 39, 45, 'f', '0')
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
