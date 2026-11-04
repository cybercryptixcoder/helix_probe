def predict(probe):
    # Beliefs (v19):
    # - Player is a 4x4 block with 0s on its facing edge, e elsewhere [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1' [E1-E60].
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 is a boundary counter: cols 0..k are '7', cols k+1..63 are '4'. The leftmost '4' is at c=k+1.
    #   Moving the boundary LEFT by one means: c=k+1 becomes '4' (was '7'), and the old leftmost '4' at c=k+2
    #   stays '4' (no change). So only ONE cell changes per counter step: the new leftmost '4' cell [E64,E66].
    # - Counter moves left by 1 on successful ACTION1 (upward move) [E46,E48,E62,E64,E66].
    # - Counter does NOT move on blocked ACTION1 [E50,E60,E67,E68].
    #   KEY FIX: E67/E68 show ACTION1 at the topmost reachable position (rows 20-23) does NOT move the counter.
    #   The player moved up (rows 16-19 became the new top block) but the counter stayed. So the counter only
    #   moves when the player's LOWEST block actually shifts up — i.e. when the player is NOT already at the
    #   topmost position. Wait: E67 moved from rows 24-27 to 20-23 (counter moved to c11). E68 moved from
    #   20-23 to 16-19 (counter did NOT move). So the boundary is: counter moves on ACTION1 only while the
    #   player's bottom edge is below row 20 (i.e. lowest block top >= 20). At lowest-block-top == 20 the
    #   counter stops. Actually E67's result: after E67 lowest block top = 20, counter at c11. E68: lowest
    #   block top goes 20->16, counter stays c11. So counter moves when lowest-block-top BEFORE the move is
    #   >= 24? Let's check: E66 (before: lowest top 28) counter moved 13->12. E67 (before: lowest top 24)
    #   counter moved 12->11. E68 (before: lowest top 20) counter did NOT move. So counter moves iff the
    #   player's lowest block top BEFORE the move is >= 24 (i.e. the move takes it from >=24 to >=20).
    #   Equivalently: counter moves on ACTION1 iff the player's bottom row (r0+3) is >= 27 before the move.
    #   Hmm, simpler: counter moves iff new lowest-block-top >= 20. E66: new top 24 >=20 yes. E67: new 20>=20 yes.
    #   E68: new 16 <20 no. That fits! Counter moves on ACTION1 iff resulting lowest-block-top >= 20.
    #   (i.e. the player does not go above row 20.)
    # - Counter does NOT move on ACTION2/3/4 [E42,E52,E54,E55,E57,E59].
    # - Counter does NOT move on ACTION5 [E51,E53,E58].
    # - Goal: ? Best guess: shift the boundary all the way left (all '4's, no '7's) via successful ACTION1s.
    actions = probe.get("actions", [])
    frame = probe.get("frame", None)
    grid = None
    if frame is not None:
        try:
            grid = [list(row) for row in frame]
        except Exception:
            grid = None

    def snap(before):
        ch = {}
        for r in range(64):
            for c in range(64):
                if grid[r][c] != before[r][c]:
                    ch["%d,%d" % (r, c)] = grid[r][c]
        return ch

    def find_player():
        best = None; bestn = -1
        for r0 in range(0, 60, 4):
            for c0 in range(0, 61, 4):
                n = 0
                for k in range(4):
                    for j in range(4):
                        v = grid[r0+k][c0+j]
                        if v in ("0", "e"):
                            n += 1
                if n > bestn:
                    bestn = n; best = (r0, c0)
        if best is None:
            return None, None
        r0, c0 = best
        top = sum(1 for j in range(4) if grid[r0][c0+j]=="0")
        bot = sum(1 for j in range(4) if grid[r0+3][c0+j]=="0")
        left = sum(1 for k in range(4) if grid[r0+k][c0]=="0")
        right = sum(1 for k in range(4) if grid[r0+k][c0+3]=="0")
        edges = {"U":top,"D":bot,"L":left,"R":right}
        facing = max(edges, key=edges.get)
        if edges[facing] == 0:
            facing = "R"
        return (r0, c0), facing

    def region_empty(r0, c0):
        if r0 < 0 or r0 > 59 or c0 < 0 or c0 > 60:
            return False
        for k in range(4):
            for j in range(4):
                if grid[r0+k][c0+j] != "1":
                    return False
        return True

    def make_band(facing):
        band = [["e"]*4 for _ in range(4)]
        if facing == "U":
            for j in range(4): band[0][j] = "0"
        elif facing == "D":
            for j in range(4): band[3][j] = "0"
        elif facing == "L":
            for k in range(4): band[k][0] = "0"
        else:
            for k in range(4): band[k][3] = "0"
        return band

    # locate counter boundary on row 63: leftmost '4' (cols left of it are '7')
    counter_col = None
    if grid is not None:
        row63 = grid[63]
        for c in range(64):
            if row63[c] == "4":
                counter_col = c
                break

    steps = []
    for a in actions:
        if grid is None:
            steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
            continue
        before = [row[:] for row in grid]
        counter_moves = False

        if a in ("ACTION1", "ACTION2", "ACTION3", "ACTION4"):
            pl, facing = find_player()
            if pl is not None:
                r0, c0 = pl
                if a == "ACTION1":
                    nr0, nc0 = r0 - 4, c0; nf = "U"
                elif a == "ACTION2":
                    nr0, nc0 = r0 + 4, c0; nf = "D"
                elif a == "ACTION3":
                    nr0, nc0 = r0, c0 - 4; nf = "L"
                else:
                    nr0, nc0 = r0, c0 + 4; nf = "R"
                if 0 <= nr0 <= 59 and 0 <= nc0 <= 60 and region_empty(nr0, nc0):
                    for k in range(4):
                        for j in range(4):
                            grid[r0+k][c0+j] = "1"
                    band = make_band(nf)
                    for k in range(4):
                        for j in range(4):
                            grid[nr0+k][nc0+j] = band[k][j]
                    # counter moves on ACTION1 iff resulting lowest-block-top >= 20
                    if a == "ACTION1" and nr0 >= 20:
                        counter_moves = True
        elif a == "ACTION5":
            pl, facing = find_player()
            if pl is not None:
                c0 = pl[1]
                for r0 in range(56, -1, -4):
                    vals = [grid[r0+k][c0+j] for k in range(4) for j in range(4)]
                    if all(v == "0" for v in vals):
                        for k in range(4):
                            for j in range(4):
                                grid[r0+k][c0+j] = "3"
                        break
                    elif all(v == "3" for v in vals):
                        for k in range(4):
                            for j in range(4):
                                grid[r0+k][c0+j] = "0"
                        break

        # counter: boundary between '7' (left) and '4' (right). Move left = one more '4'.
        if counter_col is not None and counter_col > 0 and counter_moves:
            grid[63][counter_col - 1] = "4"
            counter_col -= 1

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
