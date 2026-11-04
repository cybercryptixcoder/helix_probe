def predict(probe):
    # Model v12, based on E1-E68.
    # CLICK on a tile: select it (border 0) or deselect (border 4); selecting one deselects others [E2,E3,E6]
    # CLICK MID while a bottom tile is selected: swap MID inner <-> that tile inner, advance counter [E16,E18,E30,E34,E36,E44]
    # CLICK MID while nothing selected: select MID [E28]
    # CLICK bottom tile while MID selected: swap MID inner <-> tile inner, both borders->4, advance counter [E32,E34,E36,E42,E68]
    # CLICK bottom tile while nothing selected: select it [E1,E3]
    # ACTION5: deselect selected tile (border->4) and advance counter [E24,E26]
    # ACTION7: swap MID inner <-> SELECTED bottom tile's inner (tile1 if none selected), deselect that tile, no counter advance [E19,E49,E66,E68]
    # Counter: row 53, rightmost 3 moves left by one each swap/ACTION5 [E11,E40,E44]
    # Goal: ? unknown; not yet observed completing a level.
    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {}
    grid = [list(row) for row in frame]
    R = len(grid)
    C = len(grid[0]) if R else 0

    TILES = [(56, 61, 17, 22), (56, 61, 25, 30),
             (56, 61, 33, 38), (56, 61, 41, 46)]
    MID = (27, 32, 32, 37)

    def tile_at(x, y):
        for t in TILES:
            r0, r1, c0, c1 = t
            if r0 <= y <= r1 and c0 <= x <= c1:
                return t
        r0, r1, c0, c1 = MID
        if r0 <= y <= r1 and c0 <= x <= c1:
            return MID
        return None

    def border_cells(r0, r1, c0, c1):
        cells = set()
        for cc in range(c0, c1 + 1):
            cells.add((r0, cc)); cells.add((r1, cc))
        for rr in range(r0, r1 + 1):
            cells.add((rr, c0)); cells.add((rr, c1))
        return cells

    def inner_cells(r0, r1, c0, c1):
        return [(rr, cc) for rr in range(r0 + 1, r1)
                for cc in range(c0 + 1, c1)]

    def is_selected(t):
        r0, r1, c0, c1 = t
        return all(grid[rr][cc] == '0' for (rr, cc) in border_cells(r0, r1, c0, c1))

    def set_border(t, colour, changes):
        r0, r1, c0, c1 = t
        for (rr, cc) in border_cells(r0, r1, c0, c1):
            if grid[rr][cc] != colour:
                grid[rr][cc] = colour
                changes[f"{rr},{cc}"] = colour

    def set_inner(t, colour, changes):
        r0, r1, c0, c1 = t
        for (rr, cc) in inner_cells(r0, r1, c0, c1):
            if grid[rr][cc] != colour:
                grid[rr][cc] = colour
                changes[f"{rr},{cc}"] = colour

    def get_inner_colour(t):
        r0, r1, c0, c1 = t
        cells = inner_cells(r0, r1, c0, c1)
        if not cells:
            return None
        return grid[cells[0][0]][cells[0][1]]

    def selected_bottom():
        for t in TILES:
            if is_selected(t):
                return t
        return None

    def advance_counter(changes):
        cols3 = [cc for cc in range(C) if grid[53][cc] == '3']
        if cols3:
            newc = min(cols3) - 1
        else:
            newc = C - 1
        if 0 <= newc < C and grid[53][newc] != '3':
            grid[53][newc] = '3'
            changes[f"53,{newc}"] = '3'

    def do_swap(bottom_tile, changes):
        prev_mid = get_inner_colour(MID)
        prev_bot = get_inner_colour(bottom_tile)
        set_border(MID, '4', changes)
        set_inner(MID, prev_bot, changes)
        set_border(bottom_tile, '4', changes)
        set_inner(bottom_tile, prev_mid, changes)
        advance_counter(changes)

    steps = []
    for act in actions:
        changes = {}
        if act.startswith("CLICK"):
            try:
                parts = act.split()
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
                continue
            t = tile_at(x, y)
            if t is not None:
                if t == MID:
                    if is_selected(MID):
                        set_border(MID, '4', changes)
                    else:
                        sb = selected_bottom()
                        if sb is not None:
                            do_swap(sb, changes)
                        else:
                            set_border(MID, '0', changes)
                else:
                    if is_selected(t):
                        set_border(t, '4', changes)
                    else:
                        for other in TILES:
                            if other != t and is_selected(other):
                                set_border(other, '4', changes)
                        if is_selected(MID):
                            do_swap(t, changes)
                        else:
                            set_border(t, '0', changes)
        elif act == "ACTION5":
            sb = selected_bottom()
            if sb is not None:
                set_border(sb, '4', changes)
            elif is_selected(MID):
                set_border(MID, '4', changes)
            advance_counter(changes)
        elif act == "ACTION7":
            # swap MID inner <-> SELECTED bottom tile's inner (tile1 if none), deselect it, no counter advance [E19,E49,E66,E68]
            tgt = selected_bottom()
            if tgt is None:
                tgt = TILES[0]
            prev_mid = get_inner_colour(MID)
            prev_t = get_inner_colour(tgt)
            set_border(MID, '4', changes)
            set_inner(MID, prev_t, changes)
            set_border(tgt, '4', changes)
            set_inner(tgt, prev_mid, changes)
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
