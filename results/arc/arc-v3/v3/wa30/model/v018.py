def predict(probe):
    # Beliefs (v18):
    # - Player is a 4x4 block with 0s on its facing edge, e elsewhere [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1' [E1-E60].
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 shows a counter: a single '4' at some column, rest '1'. Counter moves LEFT by 1 on
    #   successful ACTION1 (upward move) [E46,E48,E60,E62,E64]. Counter does NOT move on blocked ACTION1 [E50,E60].
    #   Counter does NOT move on ACTION2/3/4 [E42,E52,E54,E55,E57,E59]. Counter does NOT move on ACTION5 [E51,E53,E58].
    # - Counter rendering: only ONE cell is '4'; the cell it vacates becomes '1'. [E60,E64 correct v16/v17]
    #   The bug in v17: it set the vacated cell to '1' but the "changes" diff still listed it because
    #   the previous cell was already '1' in some cases... actually the real bug: v17 wrote grid[63][counter_col]='1'
    #   then decremented, but when the vacated cell was ALREADY '1' it still appeared in the diff only if it
    #   differed. The observed shows NO r63 c14:1 change, meaning the vacated cell was already '1' and stays '1'
    #   (no change). v17 incorrectly emitted it because... it set it to '1' when it was '4' -> that IS a change.
    #   Wait: observed E64 shows r63 c13:4 only, NOT r63 c14:1. So the old '4' at c14 became '1' but that
    #   is NOT reported. That means the counter is NOT a single '4' with rest '1' — the trailing cells are
    #   NOT '1'. Re-examining: row 63 in the screen shows "7777777777777444444444444444444444444444444444444444444444444444"
    #   i.e. cols 0-12 are '7', cols 13-63 are '4'. So the counter is a BOUNDARY: '7's on the left, '4's on the right!
    #   The "4" at c13 is the leftmost '4'. Moving left by one means c13 becomes '7' and c12 becomes '4'.
    #   But observed E64 only shows r63 c13:4 — meaning c13 was NOT '4' before (it was '7'?) Hmm.
    #   Actually: before E64, row63 had '4' at c14 (from E63). After, '4' at c13. The change list shows only
    #   c13:4. So c14 must have already been '4' (it was — the whole right side is '4'). And c13 changed
    #   from '7' to '4'. So the counter is: cols 0..k are '7', cols k+1..63 are '4', and the "counter position"
    #   is the boundary. Moving left: the boundary shifts left, i.e. one more '4' on the left, one fewer '7'.
    #   So the vacated cell (old boundary+1) stays '4' — no change there. Only the new boundary cell changes 7->4.
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
                    if a == "ACTION1":
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
