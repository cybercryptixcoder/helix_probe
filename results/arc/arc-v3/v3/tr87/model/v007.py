def predict(probe):
    # Beliefs (mechanism), revised after E16-E20:
    # - 5 tiles at col spans [15-19],[22-26],[29-33],[36-40],[43-47], rows 48-60.
    #   Active tile shows 0s, inactive show 3s [E1,E3,E7,E16].
    # - ACTION3 moves active tile LEFT (wrap 0->4); ACTION4 moves RIGHT (wrap 4->0) [E1,E3,E7,E16].
    #   Only the border cells (r48,r49,r59,r60 and c-ends) change when switching tiles [E16].
    # - ACTION1/ACTION2 toggle the 5x5 interior (rows 52-56) of the ACTIVE tile, 5<->7 [E2,E6,E12,E17-E20].
    #   E20: ACTION2 changed only 8 cells in the active tile (c22 span) - a partial toggle,
    #   not the full 25-cell flip. So the interior toggle is a SPARSE pattern, not all cells.
    #   The exact sparse pattern is unknown; best guess: toggle a fixed subset of interior cells.
    # - Row 63 progress bar of 4s grows leftward, ~1 cell per action [E1,E7,E16-E20].
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
        for r in range(R0, R1 + 1):
            for c in range(a, b + 1):
                # border = rows 48,49,59,60 or cols a,b
                if r in (48, 49, 59, 60) or c in (a, b):
                    if g[r][c] in '03':
                        g[r][c] = ch
                        changes[f"{r},{c}"] = ch

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
            # Sparse interior toggle: toggle a fixed subset of the 5x5 interior.
            # E20 showed only ~8 cells change, not all 25. Use a checkerboard-ish subset.
            a, b = BOXES[active]
            for r in range(52, 57):
                for c in range(a, b + 1):
                    if (r + c) % 2 == 0 and grid[r][c] in '57':
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
