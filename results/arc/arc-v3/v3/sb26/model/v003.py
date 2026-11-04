def predict(probe):
    # Model v3, based on E1-E12.
    #
    # Screen layout (level 1):
    #  - Top area: 5 coloured boxes (9,e,b,f) at rows 1-6, cols 17-46. Inert.
    #    [E1, E3, E5, E8, E10, E11: clicking them does nothing]
    #  - Middle: a big rounded frame (colour 8) rows 24-35, cols 16-47.
    #    Inside it are 2x2 colour-2 squares at rows 29-30 (cols 21-22, 28-29,
    #    35-36, 42-43). Clicking a 2-square does nothing [E8, E11, E12].
    #  - There are also 6x6 "tile" controls drawn as 0-bordered boxes:
    #      * bottom row (rows 56-61): cols 17-22, 25-30, 33-38, 41-46
    #      * middle (rows 27-32): cols 32-37  [E11, E12]
    #    Clicking one selects it: its 0-border cells become 0 (already 0 for
    #    the middle one? no: middle one's border is 0 when selected, 4 when
    #    not). Selecting deselects any previously selected tile (border->4).
    #    Clicking a selected tile deselects it (border->4). [E1,E2,E3,E9,E10,
    #    E11, E12]
    #  - The middle tile at rows 27-32 cols 32-37: its border is 0 when
    #    selected and 4 when not (same as bottom tiles). [E11 selected it,
    #    E12 selected then deselected it]
    #  - Row 53 colour-2 line: clicking it does nothing. [E5,E6,E7,E9]
    #  - ACTION7 does nothing. [E1]
    #
    # ? Goal: unknown. Best guess: select tiles in the correct order to
    #   match some pattern. We do not predict completion yet.

    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {}
    grid = [list(row) for row in frame]
    R = len(grid)
    C = len(grid[0]) if R else 0

    # All clickable 6x6 tiles: (r0,r1,c0,c1). Border is 0 when selected,
    # original colour (4) when not.
    TILES = [(56, 61, 17, 22), (56, 61, 25, 30),
             (56, 61, 33, 38), (56, 61, 41, 46),
             (27, 32, 32, 37)]

    def tile_at(x, y):
        for t in TILES:
            r0, r1, c0, c1 = t
            if r0 <= y <= r1 and c0 <= x <= c1:
                return t
        return None

    def border_cells(r0, r1, c0, c1):
        cells = set()
        for cc in range(c0, c1 + 1):
            cells.add((r0, cc)); cells.add((r1, cc))
        for rr in range(r0, r1 + 1):
            cells.add((rr, c0)); cells.add((rr, c1))
        return cells

    def is_selected(t):
        r0, r1, c0, c1 = t
        return all(grid[rr][cc] == '0' for (rr, cc) in border_cells(r0, r1, c0, c1))

    def set_border(t, colour, changes):
        r0, r1, c0, c1 = t
        for (rr, cc) in border_cells(r0, r1, c0, c1):
            if grid[rr][cc] != colour:
                grid[rr][cc] = colour
                changes[f"{rr},{cc}"] = colour

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
                if is_selected(t):
                    set_border(t, '4', changes)
                else:
                    # deselect all currently selected tiles
                    for other in TILES:
                        if other != t and is_selected(other):
                            set_border(other, '4', changes)
                    set_border(t, '0', changes)
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
