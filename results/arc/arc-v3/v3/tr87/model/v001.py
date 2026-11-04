def predict(probe):
    # Model of the box (level 1).
    #
    # Screen layout: a 64x64 grid. The bottom row r63 is a status/indicator row.
    #   r63 c63 holds a colour that changes with actions (4 seen). [E1,E2]
    #   r63 c60..c62 also change (4 seen) - likely a cursor/position indicator. [E2]
    #
    # There are "tile" regions of 7x7 blocks (colour a=10 border, 5/7 interior).
    #   Two 7x7 tiles around r4-10 c12-18 and c22-28; same at r13-19; r22-28. [screen]
    #   A wide 7-row banner r41-47 c14-49. [screen]
    #   A 7x7 tile r51-57 c14-20 and c22-28. [screen]
    #
    # Observed action effects (from E1/E2):
    #   ACTION1: toggles the two 7x7 tiles at r48-60 c15-26 between 3<->0 borders. [E1,E2]
    #   ACTION2: toggles interior 5<->7 in the r51-57 c22-28 tile. [E1,E2]
    #   ACTION3: toggles the r48-60 c15-26 tiles 0<->3 (same region as ACTION1, opposite phase). [E1,E2]
    #   ACTION4: moves the r63 cursor left by 1 (c63->c62->c61->c60). [E1,E2]
    #
    # The exact toggle regions are uncertain; below I encode the observed cells.
    # GOAL (?): likely align the two 7x7 tiles (r48-60 c15-26) to matching colours,
    #   or move cursor to a target. Unproven - mark as guess.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    level = probe.get("level", 0)
    history = probe.get("history", [])

    # Build mutable grid from frame if provided, else empty.
    grid = None
    if frame:
        grid = [list(row) for row in frame]
    else:
        grid = [['2'] * 64 for _ in range(64)]

    def setc(r, c, v):
        if 0 <= r < 64 and 0 <= c < 64:
            grid[r][c] = v

    def getc(r, c):
        return grid[r][c]

    # Region A: the two 7x7 tiles at r48-60, c15-26 (borders at rows 48,60 and cols 15,19,22,26).
    # From E1: cells toggled 3<->0 at r48 c15-19, c22-26; r49 c15,c19,c22,c26; r59 same; r60 c15-19,c22-26.
    regionA = []
    for c in range(15, 20):
        regionA.append((48, c)); regionA.append((60, c))
    for c in range(22, 27):
        regionA.append((48, c)); regionA.append((60, c))
    for r in (49, 59):
        for c in (15, 19, 22, 26):
            regionA.append((r, c))

    # Region B: interior 5<->7 in tile r51-57 c22-28 (from E1/E2).
    regionB = [(53,22),(54,23),(55,22),(55,23),(55,25),(56,22),(56,26)]

    def toggleA():
        for (r, c) in regionA:
            v = getc(r, c)
            setc(r, c, '0' if v == '3' else '3')

    def toggleB():
        for (r, c) in regionB:
            v = getc(r, c)
            setc(r, c, '5' if v == '7' else '7')

    # Cursor position on r63: track via history (starts at c63).
    # We infer cursor from frame: find the '4' in r63.
    cursor = 63
    for c in range(64):
        if getc(63, c) == '4':
            cursor = c
            break

    steps = []
    for act in actions:
        changes = {}
        if act == 'ACTION1':
            before = {(r, c): getc(r, c) for (r, c) in regionA}
            toggleA()
            for (r, c) in regionA:
                if getc(r, c) != before[(r, c)]:
                    changes["%d,%d" % (r, c)] = getc(r, c)
        elif act == 'ACTION2':
            before = {(r, c): getc(r, c) for (r, c) in regionB}
            toggleB()
            for (r, c) in regionB:
                if getc(r, c) != before[(r, c)]:
                    changes["%d,%d" % (r, c)] = getc(r, c)
        elif act == 'ACTION3':
            before = {(r, c): getc(r, c) for (r, c) in regionA}
            toggleA()
            for (r, c) in regionA:
                if getc(r, c) != before[(r, c)]:
                    changes["%d,%d" % (r, c)] = getc(r, c)
        elif act == 'ACTION4':
            # move cursor left by 1
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
