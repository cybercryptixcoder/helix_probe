def predict(probe):
    # Model of the box (level 1).
    #
    # Screen: 64x64. Bottom row r63 is a status row.
    #   r63 c58..c63 holds a cursor (colour 4) that moves LEFT by 1 per ACTION4,
    #   leaving colour 3 behind. [E1,E2,E3]
    #
    # ACTION1: toggles the two 7x7 tiles at r48-60 c15-26 between 0<->3 borders. [E1,E2,E3]
    # ACTION2: toggles interior 5<->7 in a 7x7 tile whose position depends on the
    #   cursor column! [E2,E3]
    #     - cursor at c61 (E2): toggled tile r51-57 c22-28 (interior cells).
    #     - cursor at c58 (E3): toggled tile r51-57 c15-21 (interior cells).
    #   So ACTION2 acts on the tile under/nearest the cursor column.
    # ACTION3: toggles the r48-60 c15-26 tiles 0<->3 (opposite phase of ACTION1). [E1,E2,E3]
    # ACTION4: moves cursor left by 1 on r63. [E1,E2,E3]
    #
    # GOAL (?): likely align tiles / move cursor to a target. Unproven.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    grid = [list(row) for row in frame] if frame else [['2'] * 64 for _ in range(64)]

    def setc(r, c, v):
        if 0 <= r < 64 and 0 <= c < 64:
            grid[r][c] = v

    def getc(r, c):
        return grid[r][c]

    # Region A: borders of the two 7x7 tiles at r48-60, c15-19 and c22-26.
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

    # Interior cells of a 7x7 tile given its top-left border corner (r0,c0).
    # Border rows r0,r0+6; border cols c0,c0+6. Interior = r0+1..r0+5, c0+1..c0+5.
    def interior(r0, c0):
        return [(r, c) for r in range(r0 + 1, r0 + 6) for c in range(c0 + 1, c0 + 6)]

    def toggleB(cursor):
        # ACTION2 acts on the tile nearest the cursor column.
        # Tiles: left tile c15-21, right tile c22-28 (both r51-57).
        # Choose tile whose column span contains cursor, else nearest.
        left = (51, 15); right = (51, 22)
        if cursor <= 21:
            r0, c0 = left
        else:
            r0, c0 = right
        for (r, c) in interior(r0, c0):
            v = getc(r, c)
            setc(r, c, '5' if v == '7' else '7')

    # Cursor: find '4' in r63.
    cursor = 63
    for c in range(64):
        if getc(63, c) == '4':
            cursor = c
            break

    steps = []
    for act in actions:
        changes = {}
        if act in ('ACTION1', 'ACTION3'):
            before = {(r, c): getc(r, c) for (r, c) in regionA}
            toggleA()
            for (r, c) in regionA:
                if getc(r, c) != before[(r, c)]:
                    changes["%d,%d" % (r, c)] = getc(r, c)
        elif act == 'ACTION2':
            # snapshot interior of both tiles
            cells = interior(51, 15) + interior(51, 22)
            before = {p: getc(*p) for p in cells}
            toggleB(cursor)
            for p in cells:
                if getc(*p) != before[p]:
                    changes["%d,%d" % p] = getc(*p)
        elif act == 'ACTION4':
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
