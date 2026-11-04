def predict(probe):
    # Beliefs (mechanism), revised after E22:
    # - 5 tiles at col spans [15-19],[22-26],[29-33],[36-40],[43-47], rows 48-60.
    #   Active tile shows 0s, inactive show 3s [E1,E3,E7,E16,E22].
    # - ACTION3 moves active tile LEFT (wrap 0->4); ACTION4 moves RIGHT (wrap 4->0) [E1,E3,E7,E16].
    #   Switching changes ONLY border cells: rows 48,60 full span; rows 49,59 endpoints only [E16,E22].
    #   (Earlier model wrongly included rows 50,58 - fixed.)
    # - ACTION1/ACTION2 toggle a sparse subset of the 5x5 interior (rows 52-56) of the ACTIVE tile [E17-E22].
    #   The exact pattern differs per tile and is not a fixed relative pattern [E22 vs E21]; best guess:
    #   toggle a fixed 7-cell relative pattern per tile. "?" - uncertain.
    # - Row 63 progress bar of 4s grows leftward, ~1 cell per action [E1,E7,E16-E22].
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
        # rows 48 and 60: full span
        for c in range(a, b + 1):
            for r in (48, 60):
                if g[r][c] in '03':
                    g[r][c] = ch
                    changes[f"{r},{c}"] = ch
        # rows 49 and 59: endpoints only
        for r in (49, 59):
            for c in (a, b):
                if g[r][c] in '03':
                    g[r][c] = ch
                    changes[f"{r},{c}"] = ch

    active = find_active(grid)
    steps = []

    # Best-guess interior toggle pattern (relative offsets from tile top-left at (52,a)).
    # Derived from tile c22 ACTION1 (E21 step1). "?" uncertain; may differ per tile.
    PATTERN = [(1, 0), (2, 1), (3, 0), (3, 1), (3, 3), (4, 0), (4, 4)]

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
            for dr, dc in PATTERN:
                r = 52 + dr
                c = a + dc
                if 52 <= r <= 56 and a <= c <= b and grid[r][c] in '57':
                    grid[r][c] = '5' if grid[r][c] == '7' else '7'
                    changes[f"{r},{c}"] = grid[r][c]

        # Progress bar: shift leftmost 4 one cell left each action.
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
