def predict(probe):
    # Beliefs:
    # - Screen 64x64. Rows 0-33 bg=2, rows 34-63 bg=3 [screen].
    # - Top cards (rows 4-10,13-19,22-28) show target patterns in 5/7 with border a [screen].
    # - Bottom cards (rows 41-47) show current patterns in 5/7 with border a [screen].
    # - ACTION1/ACTION2 toggle a sparse interior subset of a tile [E36,E39,E46,E48,E50].
    #   The tile targeted is the one under the cursor column (cursor = '4' position in r63) [E48,E50].
    # - ACTION3/ACTION4 move the cursor highlight among 5 tile groups [E1,E7,E44,E45,E48].
    #   ACTION3 moves cursor right, ACTION4 moves cursor left [E44,E45,E48].
    # - The '4' counter at row63 moves left per ACTION1/ACTION2 toggle action; at c0 -> GAME_OVER [E32].
    #   ACTION3/ACTION4 do NOT move the counter [E44,E45,E48].
    # - RESET restores level and counter [E33,E38].
    # - Goal (?): bottom cards match top target cards -> WIN.

    grid = [list(row) for row in probe["frame"]]
    actions = probe.get("actions", [])

    def find_cursor(grid):
        row = grid[63]
        for c in range(63, -1, -1):
            if row[c] == '4':
                return c
        return None

    tile_bases = [14, 21, 28, 35, 42]

    # ACTION1 mask: cells toggled (relative to interior top-left). From E46/E48/E50.
    mask1 = [(0,0),(0,1),(0,3),(0,4),
             (1,0),(1,2),(1,3),
             (2,0),(2,1),(2,2),
             (3,0),
             (4,0),(4,2),(4,4)]
    mask2 = mask1

    def toggle_mask(grid, base, mask):
        changes = {}
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
        return changes

    def cursor_to_tile(cursor):
        if cursor is None:
            return 0
        best = 0
        bestd = 999
        for i, b in enumerate(tile_bases):
            d = abs(cursor - (b + 3))
            if d < bestd:
                bestd = d
                best = i
        return best

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
            cursor = find_cursor(grid)
            idx = cursor_to_tile(cursor)
            base = tile_bases[idx]
            mask = mask1 if act == "ACTION1" else mask2
            changes = toggle_mask(grid, base, mask)
            if cursor is not None and cursor > 0:
                grid[63][cursor] = '1'
                grid[63][cursor-1] = '4'
            elif cursor == 0:
                state = "GAME_OVER"
        elif act in ("ACTION3", "ACTION4"):
            cur_block = None
            for i, b in enumerate(tile_bases):
                if grid[48][b+1] == '0':
                    cur_block = i
                    break
            if cur_block is None:
                cur_block = 0
            if act == "ACTION3":
                new_block = min(4, cur_block + 1)
            else:
                new_block = max(0, cur_block - 1)
            for i, b in enumerate(tile_bases):
                old = '0' if i == cur_block else '3'
                new = '0' if i == new_block else '3'
                if old != new:
                    for r in (48, 49, 59, 60):
                        for cc in range(b+1, b+6):
                            if r in (48, 60):
                                grid[r][cc] = new
                            else:
                                if cc == b+1 or cc == b+5:
                                    grid[r][cc] = new
                            changes[f"{r},{cc}"] = grid[r][cc]

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
