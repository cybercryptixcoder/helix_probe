def predict(probe):
    # Beliefs (v22):
    # - Player is a 4x4 block with 0s on its facing edge, e elsewhere [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1' [E1-E60].
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 is a boundary counter: cols 0..k are '7', cols k+1..63 are '4'. Leftmost '4' at c=k+1.
    #   All-'7' means counter fully right (k=63, no '4' visible) [E83].
    # - Counter advances left by 1 on successful ACTION1 when resulting r0 >= 20 [E46,E48,E62,E64,E66,E67].
    #   Does NOT move on ACTION1 when resulting r0 < 20 [E50,E60,E68,E71].
    # - Counter does NOT move on ACTION2/3/4 [E42,E52,E54,E55,E57,E59].
    #   ? BUT E83 shows c63:'4' appearing after a successful ACTION4 following RESET — may be a
    #     "first successful move after RESET" rule, or counter starts at 63 and advances on any move.
    #     I model: after RESET counter=63 (all '7'); first successful move sets c63='4' (counter=62).
    # - Counter does NOT move on ACTION5 when r0 != 12 [E51,E53,E58,E70].
    # - Counter advances left by 1 on ACTION5 at topmost r0==12 every 3rd such press [E72,E74,E76,E78,E80].
    #   ? phase tracked by hidden counter of ACTION5-at-top presses; advance when count%3==0.
    # - RESET restores level-1 initial layout: player at r48-51 c32-35 facing up, static 4/9 blocks
    #   at r28-31 c16-19 and r36-39 c32-35, r40-43 c32-35 = '1', row63 all '7' [E83].
    #   ? This is the level-1 start; other levels unknown.
    # - Goal: ? Best guess: shift boundary all the way left (counter reaches col 0) via advances.
    actions = probe.get("actions", [])
    frame = probe.get("frame", None)
    history = probe.get("history", [])
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

    def build_initial():
        # Level-1 initial layout [E83]
        g = [["1"]*64 for _ in range(64)]
        # static 4/9 blocks
        def block4(r0, c0):
            for k in range(4):
                for j in range(4):
                    g[r0+k][c0+j] = "4"
            g[r0+1][c0+1] = "9"; g[r0+1][c0+2] = "9"
            g[r0+2][c0+1] = "9"; g[r0+2][c0+2] = "9"
        block4(28, 16)
        block4(36, 32)
        # player at r48-51 c32-35 facing up
        for k in range(4):
            for j in range(4):
                g[48+k][32+j] = "e"
        for j in range(4):
            g[48][32+j] = "0"
        # row 63 all 7
        for c in range(64):
            g[63][c] = "7"
        return g

    counter_col = None
    if grid is not None:
        row63 = grid[63]
        for c in range(64):
            if row63[c] == "4":
                counter_col = c
                break
        if counter_col is None:
            counter_col = 64  # all-7: counter fully right

    top_press_count = 0
    for h in history:
        if h == "ACTION5":
            top_press_count += 1

    just_reset = False
    steps = []
    for a in actions:
        if grid is None:
            steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
            continue
        before = [row[:] for row in grid]
        counter_moves = False

        if a == "RESET":
            grid = build_initial()
            counter_col = 64
            just_reset = True
            top_press_count = 0
            steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
            continue

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
                    if a == "ACTION1" and nr0 >= 20:
                        counter_moves = True
                    # ? first successful move after RESET advances counter (E83)
                    if just_reset and counter_col == 64:
                        counter_moves = True
                    just_reset = False
        elif a == "ACTION5":
            pl, facing = find_player()
            if pl is not None:
                r0, c0 = pl
                if r0 == 12:
                    top_press_count += 1
                    if top_press_count % 3 == 0:
                        counter_moves = True
                else:
                    for rr in range(56, -1, -4):
                        vals = [grid[rr+k][c0+j] for k in range(4) for j in range(4)]
                        if all(v == "0" for v in vals):
                            for k in range(4):
                                for j in range(4):
                                    grid[rr+k][c0+j] = "3"
                            break
                        elif all(v == "3" for v in vals):
                            for k in range(4):
                                for j in range(4):
                                    grid[rr+k][c0+j] = "0"
                            break

        if counter_moves and counter_col is not None and counter_col > 0:
            grid[63][counter_col - 1] = "4"
            counter_col -= 1

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
