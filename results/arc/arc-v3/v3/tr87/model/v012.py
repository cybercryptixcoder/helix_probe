def predict(probe):
    # Beliefs:
    # - 5 tiles at col spans [15-19],[22-26],[29-33],[36-40],[43-47], rows 48-60.
    #   Active tile shows 0s on border, inactive show 3s [E1,E3,E7,E16,E22,E23].
    # - ACTION3 moves active tile LEFT (wrap 0->4); ACTION4 moves RIGHT (wrap 4->0) [E1,E3,E7,E16,E23].
    #   Switching changes ONLY border cells: rows 48,60 full span; rows 49,59 endpoints only [E16,E22,E23].
    # - ACTION1 and ACTION2 BOTH toggle the SAME fixed per-tile interior set (rows 52-56) of the ACTIVE tile.
    #   The set is per-tile (depends on absolute tile position), action-independent [E22,E23,E24,E25].
    #   Toggling flips 5<->7 on exactly that set.
    # - Tile 3 pattern now taken from E27 (16 cells), NOT a copy of tile 1.
    # - Row 63 progress bar of 4s advances leftward ~1 cell per toggle action [E22,E23,E25,E26,E27];
    #   "?" irregular (E16 step2 A4 advanced; E24 step2 A2 did not) - modeled as advancing on
    #   ACTION1/ACTION2 only, best guess.
    # - GOAL ("?"): guess = progress bar reaches column 0. NOT proven.

    grid = [list(row) for row in probe["frame"]]
    actions = probe.get("actions", [])
    BOXES = [(15, 19), (22, 26), (29, 33), (36, 40), (43, 47)]
    R0, R1 = 48, 60

    def find_active(g):
        for i, (a, b) in enumerate(BOXES):
            if g[48][a] == '0':
                return i
        return 0

    def set_border(g, ch, i, changes):
        a, b = BOXES[i]
        for c in range(a, b + 1):
            for r in (48, 60):
                if g[r][c] in '03':
                    g[r][c] = ch
                    changes[f"{r},{c}"] = ch
        for r in (49, 59):
            for c in (a, b):
                if g[r][c] in '03':
                    g[r][c] = ch
                    changes[f"{r},{c}"] = ch

    # Per-tile interior toggle patterns (relative offsets from tile top-left at (52,a)).
    # Same set used by BOTH ACTION1 and ACTION2 [E22,E23,E24,E25].
    PATTERNS = {
        0: [(0, 0), (0, 1), (1, 0), (1, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 3)],  # E22,E23
        1: [(0, 4), (1, 0), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 4), (4, 0)],  # E24,E25
        2: [(0, 0), (0, 1), (1, 0), (1, 2), (2, 3), (3, 4), (4, 3), (4, 4)],  # E26
        3: [(0, 0), (0, 1), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3),
            (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 3), (3, 4), (4, 0), (4, 4)],  # E27
        4: [(0, 4), (1, 0), (1, 3), (1, 4), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 4), (4, 0)],  # "?" guessed like tile 1
    }

    active = find_active(grid)
    steps = []

    for act in actions:
        changes = {}
        if act == "ACTION3":
            old = active
            active = (active - 1) % 5
            set_border(grid, '3', old, changes)
            set_border(grid, '0', active, changes)
        elif act == "ACTION4":
            old = active
            active = (active + 1) % 5
            set_border(grid, '3', old, changes)
            set_border(grid, '0', active, changes)
        elif act in ("ACTION1", "ACTION2"):
            a, b = BOXES[active]
            for dr, dc in PATTERNS[active]:
                r = 52 + dr
                c = a + dc
                if 52 <= r <= 56 and a <= c <= b and grid[r][c] in '57':
                    grid[r][c] = '5' if grid[r][c] == '7' else '7'
                    changes[f"{r},{c}"] = grid[r][c]

        # Progress bar: advance on toggle actions only (best guess, "?").
        if act in ("ACTION1", "ACTION2"):
            row63 = grid[63]
            pos = None
            for c in range(64):
                if row63[c] == '4':
                    pos = c
                    break
            if pos is not None and pos > 0:
                row63[pos - 1] = '4'
                changes[f"63,{pos-1}"] = '4'

        done = False
        for c in range(64):
            if grid[63][c] == '4':
                done = (c <= 0)
                break
        steps.append({
            "changes": changes,
            "levels": 1 if done else 0,
            "state": "WIN" if done else "NOT_FINISHED",
        })

    return {"steps": steps}
