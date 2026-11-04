def predict(probe):
    # Model v9, based on E1-E36.
    #
    # Screen layout (level 1):
    #  - Top area: 5 coloured boxes (9,e,b,f) rows 1-6. Inert. [E1,E8,E10,E20,E21]
    #  - Middle frame (colour 8) rows 24-35. Inner 2x2 colour-2 squares inert. [E8,E12]
    #  - Row 53 colour-2 line: clicking does nothing. [E5,E6,E9]
    #  - Bottom-row tiles (6x6, 0-bordered) at rows 56-61, cols 17-22,25-30,33-38,41-46.
    #    Clicking selects (border->0), deselects others. Clicking selected deselects. [E1,E2,E9,E11,E22]
    #  - Middle tile rows 27-32 cols 32-37: clicking toggles selection (border 0<->4). [E11,E12,E28]
    #  - A "swap" happens when a bottom tile is clicked while the middle is selected, OR the
    #    middle is clicked while a bottom tile is selected. In a swap:
    #      * middle border->4, middle inner shows the clicked bottom tile's own colour
    #      * bottom border->4, bottom inner shows the PREVIOUS middle inner colour
    #      * counter advances. [E14,E16,E18,E30,E32,E34,E36]
    #    ? The "previous middle inner colour" is the colour in the middle inner just before
    #      this click. If the middle inner was empty (4), use the clicked tile's colour. [E32]
    #    NOTE: the middle inner ALWAYS becomes the clicked bottom's own colour, regardless
    #      of what the middle inner held before. [E36: middle had f, clicked e-tile -> middle
    #      inner became e, not f]
    #  - Clicking a bottom tile while middle NOT selected: just selects it (border->0). [E29]
    #  - ACTION5: deselects selected bottom/middle tile (border->4), advances counter. [E24,E28,E30]
    #    If nothing selected, still advances counter. [E23,E26]
    #  - Counter: one colour-3 cell on row 53, marching left from c63. [E23,E24,E26,E28,E30]
    #  - ACTION7 does nothing. [E1,E19]
    #
    # ? Goal: unknown. Best guess: complete when all four bottom tiles' inner 4x4 show their
    #   own colour (a colour-matching puzzle), OR the counter reaches the left end. Not predicted.

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
        # middle inner <- clicked bottom's own colour
        # bottom inner <- previous middle inner colour (or clicked tile's colour if empty)
        prev_mid = get_inner_colour(MID)
        if prev_mid is None or prev_mid == '4':
            prev_mid = TILE_COLOUR[bottom_tile]
        set_border(MID, '4', changes)
        set_inner(MID, TILE_COLOUR[bottom_tile], changes)
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
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
