def predict(probe):
    # Beliefs:
    # - 5 tiles at col spans [15-19],[22-26],[29-33],[36-40],[43-47], rows 48-60.
    #   Active tile shows 0s on border, inactive show 3s [E1,E3,E7,E16,E22,E23].
    # - ACTION3 moves active tile LEFT (wrap 0->4); ACTION4 moves RIGHT (wrap 4->0) [E1,E3,E7,E16,E23].
    #   Switching changes ONLY border cells: rows 48,60 full span; rows 49,59 endpoints only [E16,E22,E23].
    # - ACTION1/ACTION2 toggle a sparse subset of the 5x5 interior (rows 52-56) of the ACTIVE tile.
    #   The pattern is per-tile (depends on absolute position), not a fixed relative pattern [E22 vs E21].
    #   Best guess: each tile has its own fixed toggle set; we store per-tile patterns learned from evidence.
    #   "?" - uncertain for unseen tiles.
    # - Row 63 progress bar of 4s grows leftward, ~1 cell per action [E1,E7,E16-E23].
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
    # Derived from observed ACTION1/ACTION2 toggles per tile. "?" uncertain for tiles 3,4.
    # Tile 0 (c15): from E22/E23 -> {(0,0),(0,1),(1,0),(1,2),(3,0),(3,1),(3,2),(3,3),(4,0),(4,3)}
    # Tile 1 (c22): from E17-E21 -> {(1,0),(2,1),(3,0),(3,1),(3,3),(4,0),(4,4)}
    # Tile 2 (c29): from E12 -> approximate; "?" uncertain
    PATTERNS = {
        0: [(0, 0), (0, 1), (1, 0), (1, 2), (3, 0), (3, 1), (3, 2), (3, 3), (4, 0), (4, 3)],
        1: [(1, 0), (2, 1), (3, 0), (3, 1), (3, 3), (4, 0), (4, 4)],
        2: [(0, 0), (0, 1), (0, 3), (1, 1), (1, 2), (2, 2), (3, 1), (3, 2), (4, 0), (4, 3)],
        3: [(1, 0), (2, 1), (3, 0), (3, 1), (3, 3), (4, 0), (4, 4)],
        4: [(1, 0), (2, 1), (3, 0), (3, 1), (3, 3), (4, 0), (4, 4)],
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

        row63 = grid[63]
        pos = None
        for c in range(64):
            if row63[c] == '4':
                pos = c
                break
        if pos is not None and pos > 0:
            row63[pos - 1] = '4'
            changes[f"63,{pos-1}"] = '4'

        done = (pos is not None and pos <= 1)
        steps.append({
            "changes": changes,
            "levels": 1 if done else 0,
            "state": "WIN" if done else "NOT_FINISHED",
        })

    return {"steps": steps}
