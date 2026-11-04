def predict(probe):
    # Model v2, based on E1, E2, E3.
    #
    # Screen layout (level 1):
    #  - Top area: 5 coloured boxes (9,e,b,f) at rows 1-6, cols 17-46.
    #  - Middle: a big rounded frame (colour 8) rows 24-35, cols 16-47,
    #    with 4 small 2x2 colour-2 squares inside at rows 29-30.
    #  - A horizontal line of colour 2 at row 53.
    #  - Bottom: a row of small boxes at rows 56-61: cols 17-22, 25-30,
    #    33-38, 41-46 (colour 4), and a 0-outlined box at cols 32-37
    #    rows 56-61 containing e,f,9,b tiles.
    #
    # Rules found:
    #  - Clicking a bottom-row tile (rows 56-61) selects it: its border
    #    cells become 0, and any previously selected tile reverts to 4.
    #    [E1: click 28 59 selects cols 25-30; click 20 59 selects 17-22
    #     and reverts 25-30. E2: clicking selected tile reverts it. E3:
    #     click 44 59 selects 41-46; click 36 59 selects 33-38 and
    #     reverts 41-46.]
    #  - Clicking a top-area box (rows 1-6) does nothing. [E1: click 21 4;
    #    E3: click 35 4.]
    #  - ACTION7 does nothing. [E1]
    #  - Clicking the 0-outlined box at cols 32-37 rows 56-61 does nothing
    #    (it's a container, not a tile). [E3: click 36 59 did nothing to
    #    it; actually 36 59 is inside cols 33-38 tile... see below.]
    #
    # Wait: E3 click 36 59 selected cols 33-38 (not the 0-box). The 0-box
    # is at cols 32-37 rows 56-61, overlapping. The click at x=36 y=59
    # hit the cols 33-38 tile. The 0-box at cols 32-37 is drawn *behind*
    # / around the e,f,9,b tiles at rows 57-60.
    #
    # ? Goal: unknown. Best guess: select tiles in the correct order, or
    #   match the e/f/9/b tiles. We don't predict completion.

    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {}
    grid = [list(row) for row in frame]
    R = len(grid)
    C = len(grid[0]) if R else 0

    # The four clickable bottom tiles: (r0,r1,c0,c1) with original colour 4.
    TILES = [(56, 61, 17, 22), (56, 61, 25, 30),
             (56, 61, 33, 38), (56, 61, 41, 46)]

    def tile_at(x, y):
        for (r0, r1, c0, c1) in TILES:
            if r0 <= y <= r1 and c0 <= x <= c1:
                return (r0, r1, c0, c1)
        return None

    def border_cells(r0, r1, c0, c1):
        cells = set()
        for cc in range(c0, c1 + 1):
            cells.add((r0, cc)); cells.add((r1, cc))
        for rr in range(r0, r1 + 1):
            cells.add((rr, c0)); cells.add((rr, c1))
        return cells

    # Infer currently selected tile: a tile whose border is all '0'.
    selected = None
    for (r0, r1, c0, c1) in TILES:
        if all(grid[rr][cc] == '0' for (rr, cc) in border_cells(r0, r1, c0, c1)):
            selected = (r0, r1, c0, c1)
            break

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
                r0, r1, c0, c1 = t
                if selected == t:
                    # deselect: revert to 4
                    for (rr, cc) in border_cells(r0, r1, c0, c1):
                        if grid[rr][cc] != '4':
                            grid[rr][cc] = '4'
                            changes[f"{rr},{cc}"] = '4'
                    selected = None
                else:
                    # deselect previous
                    if selected is not None:
                        pr0, pr1, pc0, pc1 = selected
                        for (rr, cc) in border_cells(pr0, pr1, pc0, pc1):
                            if grid[rr][cc] != '4':
                                grid[rr][cc] = '4'
                                changes[f"{rr},{cc}"] = '4'
                    # select new: border -> 0
                    for (rr, cc) in border_cells(r0, r1, c0, c1):
                        if grid[rr][cc] != '0':
                            grid[rr][cc] = '0'
                            changes[f"{rr},{cc}"] = '0'
                    selected = t
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
