def predict(probe):
    # Model of the box (level 1).
    #
    # Screen: 64x64. Bottom row r63 is a status row.
    #
    # Cursor: a single '4' on r63. It moves LEFT by 1 per ACTION4, leaving '3'
    #   behind. [E1,E2,E3,E4,E5,E6,E7]
    #   BUT: ACTION1, ACTION2, ACTION3 ALSO move the cursor left by 1! [E1,E2,E3,E4,E5,E6,E7]
    #   Evidence: E7 (single ACTION3) moved cursor c53->c52. E3 ACTION4 moved c60->c59.
    #   E4: ACTION2 moved c58->c57, ACTION4 c57->c56, ACTION2 c56->c55, ACTION4 c55->c54, ACTION4 c54->c53.
    #   So EVERY action moves the cursor left by 1 (leaving 3). [E1..E7]
    #
    # ACTION1: toggles the pair of 7x7 tiles at r48-60 c15-19 / c22-26 (0<->3 borders). [E1,E2,E3]
    # ACTION3: toggles the SAME pair of tiles 0<->3 (opposite phase of ACTION1). [E1,E2,E3,E5,E6,E7]
    #   Note: ACTION1 and ACTION3 both toggle the SAME two tiles (c15-19 and c22-26).
    #   They do NOT toggle different tiles. [E1,E2,E3,E5,E6,E7]
    #
    # ACTION2: toggles interior 5<->7 of a 7x7 tile whose position depends on cursor column. [E2..E6]
    #   The tile is chosen by the cursor column at the time of the action.
    #   Observed tile positions (interior 5x5, border 7x7):
    #     cursor c61 -> tile r51-57 c22-28  [E2]
    #     cursor c58 -> tile r51-57 c15-21  [E3]
    #     cursor c57 -> tile r51-57 c15-21  [E4]
    #     cursor c55 -> tile r51-57 c22-28  [E4]
    #     cursor c55 -> tile r51-57 c29-35  [E5]
    #     cursor c54 -> tile r51-57 c29-35  [E6]
    #     cursor c53 -> tile r51-57 c22-28  [E6]
    #   Hmm, the tile position is NOT simply "nearest cursor".
    #   Let's tabulate: c61->c22, c58->c15, c57->c15, c55->c22, c55->c29, c54->c29, c53->c22.
    #   This looks like the tile is a function of cursor column modulo something, OR
    #   the tiles cycle. Tile left edges seen: 15, 22, 29 (step 7).
    #   c61->22, c58->15, c57->15, c55->22, c55->29, c54->29, c53->22.
    #   Try: tile index = f(cursor). 15,22,29 -> indices 0,1,2.
    #   c61->1, c58->0, c57->0, c55->1, c55->2, c54->2, c53->1.
    #   Not a clean function of cursor alone (c55 gives both 1 and 2).
    #   So ACTION2's tile depends on HISTORY, not just cursor. [E4,E5,E6]
    #   Possibly a counter that increments each ACTION2, cycling through tiles 0,1,2.
    #   E4: ACTION2 at c58 -> tile0 (15). ACTION2 at c56 -> tile1 (22).
    #   E5: ACTION2 at c55 -> tile2 (29).
    #   E6: ACTION2 at c54 -> tile2 (29). ACTION2 at c53 -> tile1 (22).
    #   Hmm E6: first ACTION2 -> tile2, second -> tile1. Not monotone.
    #   This is uncertain. Best guess: ACTION2 tile cycles 0,1,2,0,1,2... per ACTION2 count.
    #   Let's check: count ACTION2s across history.
    #   E2: 1st ACTION2 -> tile1 (22). E3: 1st -> tile0 (15). E4: 1st->tile0, 2nd->tile1.
    #   E5: 1st->tile2. E6: 1st->tile2, 2nd->tile1.
    #   Not consistent with a global counter either.
    #   Given uncertainty, use nearest-tile heuristic as fallback but note it's "?".
    #
    # GOAL (?): unknown. Possibly align tiles / reach a target. Unproven.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", [])
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

    def interior(r0, c0):
        return [(r, c) for r in range(r0 + 1, r0 + 6) for c in range(c0 + 1, c0 + 6)]

    # Cursor: find '4' in r63.
    cursor = 63
    for c in range(64):
        if getc(63, c) == '4':
            cursor = c
            break

    # Count ACTION2s in history to guess tile cycling (uncertain).
    a2count = sum(1 for a in history if a == 'ACTION2')

    def toggleB(cur, a2n):
        # Best guess: tile cycles 0,1,2 based on ACTION2 count; fallback nearest.
        # Tiles left edges: 15, 22, 29.
        # Use nearest-tile by cursor as primary heuristic (uncertain "?").
        # Nearest among 15,22,29 to cursor:
        edges = [15, 22, 29]
        best = min(edges, key=lambda e: abs((e + 3) - cur))
        r0, c0 = 51, best
        for (r, c) in interior(r0, c0):
            v = getc(r, c)
            setc(r, c, '5' if v == '7' else '7')

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
            cells = []
            for e in (15, 22, 29):
                cells += interior(51, e)
            before = {p: getc(*p) for p in cells}
            toggleB(cursor, a2count)
            a2count += 1
            for p in cells:
                if getc(*p) != before[p]:
                    changes["%d,%d" % p] = getc(*p)
        # EVERY action moves cursor left by 1 (ACTION1,2,3,4 all do).
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
