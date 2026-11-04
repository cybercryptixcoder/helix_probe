def predict(probe):
    # Model v4 (level 1).
    # Screen 64x64. Bottom row r63: block of 4s; leftmost 4 = cursor.
    # Every action moves cursor LEFT by 1: old cell -> '3', new cell -> '4'. [E1..E10]
    #   (Some steps show no r63 change when the cell to the left was already '4'? "?")
    # ACTION1 toggles region-A tiles (borders of 7x7 tiles at c15-19 & c22-26, r48-60). [E1,E2,E3]
    # ACTION3 toggles the SAME region-A tiles (opposite phase). [E1,E2,E3,E5,E6,E7,E9]
    # ACTION4 ALSO toggles region-A tiles. [E1 step1, step4]
    # ACTION2 toggles interior (5<->7) of a 7x7 tile chosen by cursor column. [E2..E10]
    #   Observed cursor->tile-left: 57->15,55->22,54->29,53->22,51->15,50->22,49->22,48->29,47->29,46->36.
    #   Best guess: tile_left = 7*floor((cursor-1)/7) - 7*? ; use nearest of {15,22,29,36} by cursor "?"
    # GOAL (?): unknown; possibly align all tiles to same phase. Unproven.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", [])
    grid = [list(row) for row in frame] if frame else [['2'] * 64 for _ in range(64)]

    def setc(r, c, v):
        if 0 <= r < 64 and 0 <= c < 64:
            grid[r][c] = v

    def getc(r, c):
        return grid[r][c]

    regionA = []
    for c in range(15, 20):
        regionA.append((48, c)); regionA.append((60, c))
    for c in range(22, 27):
        regionA.append((48, c)); regionA.append((60, c))
    for r in (49, 59):
        for c in (15, 19, 22, 26):
            regionA.append((r, c))

    def toggleA():
        for (r, c) in regionA:
            v = getc(r, c)
            setc(r, c, '0' if v == '3' else '3')

    def interior(r0, c0):
        return [(r, c) for r in range(r0 + 1, r0 + 6) for c in range(c0 + 1, c0 + 6)]

    cursor = 63
    for c in range(64):
        if getc(63, c) == '4':
            cursor = c
            break

    def tile_for_cursor(cur):
        # Best guess "?": choose tile whose span [left,left+6] is nearest to cursor.
        edges = [15, 22, 29, 36]
        return min(edges, key=lambda e: abs((e + 3) - cur))

    steps = []
    for act in actions:
        changes = {}
        if act in ('ACTION1', 'ACTION3', 'ACTION4'):
            before = {(r, c): getc(r, c) for (r, c) in regionA}
            toggleA()
            for (r, c) in regionA:
                if getc(r, c) != before[(r, c)]:
                    changes["%d,%d" % (r, c)] = getc(r, c)
        elif act == 'ACTION2':
            c0 = tile_for_cursor(cursor)
            cells = interior(51, c0)
            before = {p: getc(*p) for p in cells}
            for (r, c) in cells:
                v = getc(r, c)
                setc(r, c, '5' if v == '7' else '7')
            for p in cells:
                if getc(*p) != before[p]:
                    changes["%d,%d" % p] = getc(*p)
        if act in ('ACTION1', 'ACTION2', 'ACTION3', 'ACTION4'):
            old = cursor
            new = max(0, cursor - 1)
            if new != old:
                setc(63, old, '3')
                setc(63, new, '4')
                changes["63,%d" % old] = '3'
                changes["63,%d" % new] = '4'
                cursor = new
        elif act == 'RESET':
            pass
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})

    return {"steps": steps}
