def predict(probe):
    # Model v1, based on E1.
    #
    # Observations from E1 (start screen = the one shown above):
    #  - CLICK 28 59: the small box at rows 56-61, cols 25-30 (a "tile"
    #    drawn in colour 0 outline) turned to colour 0 fill. Actually the
    #    cells r56 c25-30, r57 c25, r57 c30, r58 c25, r58 c30, r59 c25,
    #    r59 c30, r60 c25, r60 c30, r61 c25-30 changed to 0. That is the
    #    outline of the box at cols 25-30 -> clicked it, it got "selected"
    #    (drawn as 0).
    #  - ACTION7: nothing changed.
    #  - CLICK 21 4: nothing changed (that's a top-row object, no effect).
    #  - CLICK 20 59: the box at cols 17-22 became 0 outline AND the box at
    #    cols 25-30 reverted to 4 (its original colour). So clicking a box
    #    selects it (0 outline) and deselects the previously selected box.
    #
    # So: there are several "tiles" (small rectangles). Clicking a tile
    # selects it: its outline cells become 0. The previously selected tile
    # is restored to its original colour. ACTION7 does nothing here.
    #
    # ? The goal is presumably to select tiles in some order / all of them,
    #   or to match colours. Unknown. Best guess: selecting the right tile
    #   (or sequence) completes the level. We can't yet predict completion,
    #   so we never predict levels>0.

    import copy
    frame = probe.get("frame")
    actions = probe.get("actions", [])
    if frame is None:
        return {}
    grid = [list(row) for row in frame]
    R = len(grid)
    C = len(grid[0]) if R else 0

    # Find tile rectangles: connected components of non-background colour
    # that form small boxes. We instead detect tiles by their outline:
    # a rectangle of a single colour with a hollow interior.
    # Simpler: precompute candidate tiles as bounding boxes of the small
    # objects seen in the start screen. But predict must work from any
    # frame, so detect rectangles generically.

    def find_tiles(g):
        # Find maximal rectangles of uniform colour that are "hollow":
        # border cells same colour, interior different. Return list of
        # (r0,r1,c0,c1,colour).
        tiles = []
        seen = set()
        for r in range(R):
            for c in range(C):
                col = g[r][c]
                if col in ('4', '5', '2', '8'):  # background-ish
                    continue
                if (r, c) in seen:
                    continue
                # try to grow a rectangle with uniform border of colour col
                # find extent right and down
                c2 = c
                while c2 + 1 < C and g[r][c2 + 1] == col:
                    c2 += 1
                r2 = r
                while r2 + 1 < R and g[r2 + 1][c] == col:
                    r2 += 1
                if r2 - r < 2 or c2 - c < 2:
                    continue
                # check border uniform
                ok = True
                for cc in range(c, c2 + 1):
                    if g[r][cc] != col or g[r2][cc] != col:
                        ok = False
                        break
                if ok:
                    for rr in range(r, r2 + 1):
                        if g[rr][c] != col or g[rr][c2] != col:
                            ok = False
                            break
                if not ok:
                    continue
                # mark
                for rr in range(r, r2 + 1):
                    for cc in range(c, c2 + 1):
                        seen.add((rr, cc))
                tiles.append((r, r2, c, c2, col))
        return tiles

    def tile_at(tiles, x, y):
        for t in tiles:
            r0, r1, c0, c1, col = t
            if r0 <= y <= r1 and c0 <= x <= c1:
                return t
        return None

    steps = []
    selected = None  # (r0,r1,c0,c1,origcolour) currently selected
    # We don't know selection state from frame alone; infer: a tile whose
    # border is all '0' is selected.
    tiles = find_tiles(grid)
    for t in tiles:
        r0, r1, c0, c1, col = t
        if col == '0':
            selected = t

    for act in actions:
        changes = {}
        if act.startswith("CLICK"):
            try:
                parts = act.split()
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
                continue
            tiles = find_tiles(grid)
            t = tile_at(tiles, x, y)
            if t is not None:
                r0, r1, c0, c1, col = t
                # deselect previous
                if selected is not None:
                    pr0, pr1, pc0, pc1, pcol = selected
                    for cc in range(pc0, pc1 + 1):
                        for rr in (pr0, pr1):
                            if grid[rr][cc] != pcol:
                                grid[rr][cc] = pcol
                                changes[f"{rr},{cc}"] = pcol
                    for rr in range(pr0, pr1 + 1):
                        for cc in (pc0, pc1):
                            if grid[rr][cc] != pcol:
                                grid[rr][cc] = pcol
                                changes[f"{rr},{cc}"] = pcol
                # select new: border -> 0
                for cc in range(c0, c1 + 1):
                    for rr in (r0, r1):
                        if grid[rr][cc] != '0':
                            grid[rr][cc] = '0'
                            changes[f"{rr},{cc}"] = '0'
                for rr in range(r0, r1 + 1):
                    for cc in (c0, c1):
                        if grid[rr][cc] != '0':
                            grid[rr][cc] = '0'
                            changes[f"{rr},{cc}"] = '0'
                selected = (r0, r1, c0, c1, col)
        # ACTION7 and others: no change (per E1)
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
