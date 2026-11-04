def predict(probe):
    # Model v4, based on E1-E24.
    #
    # Screen layout (level 1):
    #  - Top area: 5 coloured boxes (9,e,b,f) at rows 1-6, cols 17-46. Inert.
    #    [E1,E3,E5,E8,E10,E11,E20,E21: clicking them does nothing]
    #  - Middle: big rounded frame (colour 8) rows 24-35, cols 16-47.
    #    Inside: 2x2 colour-2 squares rows 29-30. Clicking them does nothing.
    #    [E8,E11,E12]
    #  - Row 53 colour-2 line: clicking it does nothing. [E5,E6,E7,E9]
    #  - Bottom-row tiles (6x6, 0-bordered): cols 17-22,25-30,33-38,41-46 at
    #    rows 56-61. Clicking selects (border->0), deselects others.
    #    Clicking a selected tile deselects it. [E1,E2,E3,E9,E10,E11,E12,E22]
    #  - Middle tile rows 27-32 cols 32-37: clicking selects/deselects it
    #    (border 0<->4). [E11,E12,E14,E16,E18,E20,E22]
    #  - Selecting a bottom tile while middle tile is selected: middle tile
    #    deselects (border->4) AND its inner 4x4 (rows 28-31, cols 33-36)
    #    shows the bottom tile's colour. [E11,E14,E16,E18,E19,E22]
    #    Colour map: tile1(17-22)->9, tile2(25-30)->b, tile3(33-38)->e,
    #    tile4(41-46)->f. [E11:9, E14:b/e, E16:b, E18:e, E19:e, E22:none]
    #  - Selecting the middle tile while a bottom tile is selected: middle
    #    tile border->0, inner 4x4 shows that bottom tile's colour, and the
    #    bottom tile deselects (border->4). [E14,E16,E18]
    #  - ACTION5: acts on the currently selected bottom tile (if any):
    #    deselects it (border->4) and advances a counter shown on row 53
    #    (a colour-3 cell marching left from c63). [E23,E24]
    #    If no bottom tile selected, ACTION5 still advances the counter.
    #    [E23: no tile selected, counter advanced c58->? actually E23 shows
    #     c58:3 appearing; E24 shows c57 then c56]
    #    Counter: each ACTION5 adds one colour-3 cell on row 53, moving left
    #    from c63. [E23 c58, E24 c57 then c56]
    #  - ACTION7 does nothing. [E1,E19]
    #
    # ? Goal: unknown. Best guess: press ACTION5 some number of times to
    #   fill the row-53 counter (maybe 8 cells, c56-c63). We do not predict
    #   completion yet.

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
    # colour shown in middle tile inner 4x4 for each bottom tile
    TILE_COLOUR = {(56, 61, 17, 22): '9', (56, 61, 25, 30): 'b',
                   (56, 61, 33, 38): 'e', (56, 61, 41, 46): 'f'}

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

    def selected_bottom():
        for t in TILES:
            if is_selected(t):
                return t
        return None

    def advance_counter(changes):
        # find leftmost colour-3 cell on row 53; place new one just left
        cols3 = [cc for cc in range(C) if grid[53][cc] == '3']
        if cols3:
            newc = min(cols3) - 1
        else:
            newc = C - 1
        if 0 <= newc < C and grid[53][newc] != '3':
            grid[53][newc] = '3'
            changes[f"53,{newc}"] = '3'

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
                            set_border(sb, '4', changes)
                        set_border(MID, '0', changes)
                        if sb is not None:
                            set_inner(MID, TILE_COLOUR[sb], changes)
                else:
                    if is_selected(t):
                        set_border(t, '4', changes)
                    else:
                        for other in TILES:
                            if other != t and is_selected(other):
                                set_border(other, '4', changes)
                        if is_selected(MID):
                            set_border(MID, '4', changes)
                            set_inner(MID, TILE_COLOUR[t], changes)
                        set_border(t, '0', changes)
        elif act == "ACTION5":
            sb = selected_bottom()
            if sb is not None:
                set_border(sb, '4', changes)
            advance_counter(changes)
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
