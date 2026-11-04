def predict(probe):
    # Beliefs:
    # - Screen 64x64. Rows 0-33 bg=2, rows 34-63 bg=3 [screen].
    # - Top cards (rows 4-10,13-19,22-28) show target patterns [screen].
    # - Bottom cards (rows 41-47) show current patterns; 5 tiles at bases 14,21,28,35,42 [screen].
    # - Highlight (r48-49,r59-60): active tile=0, others=3. ACTION4 moves active right (wrap 4->0),
    #   ACTION3 moves active left (wrap 0->4) [E48,E51,E53,E54].
    # - ACTION1/ACTION2 toggle a fixed interior mask on the ACTIVE (highlighted) tile [E50,E52,E54].
    # - Cursor '4' at r63 is a separate counter; ACTION1/ACTION2 move it left by 1, leaving '1' [E42,E46].
    #   At c0 -> GAME_OVER. RESET restores cursor to c60 and active tile to 0 [E48,E50].
    # - Goal (?): bottom cards match top target cards -> WIN.

    grid = [list(row) for row in probe["frame"]]
    actions = probe.get("actions", [])

    tile_bases = [14, 21, 28, 35, 42]

    def find_active(grid):
        for i, b in enumerate(tile_bases):
            if grid[48][b+1] == '0':
                return i
        return 0

    def find_cursor(grid):
        row = grid[63]
        for c in range(63, -1, -1):
            if row[c] == '4':
                return c
        return None

    # mask from E50 (relative to interior top-left at r52, c=base+1)
    mask = [(0,0),(0,1),(0,3),(0,4),
            (1,0),(1,2),(1,3),
            (2,0),(2,1),(2,2),
            (3,0),
            (4,2),(4,4)]

    def set_highlight(grid, old, new, changes):
        for i, b in enumerate(tile_bases):
            old_v = '0' if i == old else '3'
            new_v = '0' if i == new else '3'
            if old_v != new_v:
                for r in (48, 49, 59, 60):
                    for cc in range(b, b+7):
                        if r in (48, 60):
                            grid[r][cc] = new_v
                            changes[f"{r},{cc}"] = new_v
                        else:
                            if cc == b or cc == b+6:
                                grid[r][cc] = new_v
                                changes[f"{r},{cc}"] = new_v

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
                state = "NOT_FINISHED"
            steps.append({"changes": {}, "levels": levels_done, "state": state})
            continue

        if act == "RESET":
            state = "NOT_FINISHED"
            steps.append({"changes": {}, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION1", "ACTION2"):
            idx = find_active(grid)
            base = tile_bases[idx]
            c0 = base + 1
            for (dr, dc) in mask:
                r = 52 + dr
                c = c0 + dc
                if 0 <= r < 64 and 0 <= c < 64:
                    if grid[r][c] == '5':
                        grid[r][c] = '7'
                    elif grid[r][c] == '7':
                        grid[r][c] = '5'
                    changes[f"{r},{c}"] = grid[r][c]
            # cursor moves left
            cur = find_cursor(grid)
            if cur is not None:
                if cur > 0:
                    grid[63][cur] = '1'
                    grid[63][cur-1] = '4'
                else:
                    state = "GAME_OVER"
        elif act in ("ACTION3", "ACTION4"):
            cur_tile = find_active(grid)
            if act == "ACTION4":
                new_tile = (cur_tile + 1) % 5
            else:
                new_tile = (cur_tile - 1) % 5
            set_highlight(grid, cur_tile, new_tile, changes)

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
