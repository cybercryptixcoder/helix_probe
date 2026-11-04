def predict(probe):
    # Beliefs:
    # - Screen 64x64. Rows 0-33 bg=2, rows 34-63 bg=3 [screen].
    # - Top cards (rows 4-10,13-19,22-28) show target patterns [screen].
    # - Bottom cards (rows 41-47) show current patterns; 5 tiles at bases 14,21,28,35,42 [screen].
    # - Highlight is a 5-wide rectangle outline on the active tile: rows 48 & 60 full (base+1..base+5),
    #   rows 49 & 59 only at base+1 and base+5. Active tile=0, others=3 [E45,E49,E51,E53].
    # - ACTION4 moves active right (wrap 4->0), ACTION3 moves active left (wrap 0->4) [E48,E51,E53,E54].
    # - ACTION1/ACTION2 toggle the SAME interior cell subset on the ACTIVE tile (exact inverses) [E57].
    #   The subset is content-dependent: it toggles cells currently '5'->'7' and '7'->'5' within a
    #   fixed 5x5 interior region, but the observed sets vary with tile contents [E56,E57,E58].
    #   Best guess "?": toggle the full 5x5 interior (all 25 cells) of the active tile.
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

    # "?" best guess: toggle full 5x5 interior of the active tile
    mask = [(dr, dc) for dr in range(5) for dc in range(5)]

    def set_highlight(grid, old, new, changes):
        for i, b in enumerate(tile_bases):
            old_v = '0' if i == old else '3'
            new_v = '0' if i == new else '3'
            if old_v != new_v:
                for cc in range(b+1, b+6):
                    for r in (48, 60):
                        grid[r][cc] = new_v
                        changes[f"{r},{cc}"] = new_v
                for r in (49, 59):
                    for cc in (b+1, b+5):
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
