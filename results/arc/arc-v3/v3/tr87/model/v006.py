def predict(probe):
    # Beliefs (mechanism):
    # - 5 boxes at col ranges [15-19],[22-26],[29-33],[36-40],[43-47], rows 48-60.
    #   Active box shows 0s, inactive show 3s [E1,E3,E7].
    # - ACTION3 moves active box LEFT (wrap 0->4) [E1,E3,E7].
    # - ACTION4 moves active box RIGHT (wrap 4->0) [E1,E16].
    # - ACTION1/ACTION2 alter the 5x5 (rows 52-56) pattern (5<->7) in active box [E2,E6,E12].
    # - Row 63 has a progress bar of 4s growing from c63 leftward; each action advances it
    #   by ~1 (exact rule uncertain: E1 shows c63,c62; E7 shows c52 after 24 actions) [E1,E7].
    # - GOAL ("?"): guess = progress bar fills to c0 (or all boxes solved); NOT proven.

    grid = [list(row) for row in probe["frame"]]
    actions = probe.get("actions", [])
    BOXES = [(15, 19), (22, 26), (29, 33), (36, 40), (43, 47)]
    R0, R1 = 48, 60

    def find_active(g):
        for i, (a, b) in enumerate(BOXES):
            if g[48][a] == '0':
                return i
        return 0

    def set_box(g, ch, i, changes):
        a, b = BOXES[i]
        for r in range(R0, R1 + 1):
            for c in range(a, b + 1):
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
            set_box(grid, '3', old, changes)
            set_box(grid, '0', active, changes)
        elif act == "ACTION4":
            old = active
            active = (active + 1) % 5
            set_box(grid, '3', old, changes)
            set_box(grid, '0', active, changes)
        elif act in ("ACTION1", "ACTION2"):
            a, b = BOXES[active]
            for r in range(52, 57):
                for c in range(a, b + 1):
                    if grid[r][c] in '57':
                        grid[r][c] = '5' if grid[r][c] == '7' else '7'
                        changes[f"{r},{c}"] = grid[r][c]
        # RESET: leave as-is (unknown full restart) - best guess no visible change here.

        # Progress bar: shift leftmost 4 one cell left (grow bar) each action.
        row63 = grid[63]
        pos = None
        for c in range(64):
            if row63[c] == '4':
                pos = c
                break
        if pos is not None and pos > 0:
            row63[pos - 1] = '4'
            changes[f"63,{pos-1}"] = '4'

        # Goal guess: bar reaches column 0.
        done = (pos is not None and pos <= 1)
        steps.append({
            "changes": changes,
            "levels": 1 if done else 0,
            "state": "WIN" if done else "NOT_FINISHED",
        })

    return {"steps": steps}
