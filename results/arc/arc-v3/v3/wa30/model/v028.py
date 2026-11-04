def predict(probe):
    # Beliefs (v28):
    # - Player is a 4x4 block of 'e' with a 4-cell '0' edge on its facing side [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1'
    #   (row 63 is the counter row and is ignored/overwritten) [E1-E60].
    # - SPECIAL: ACTION2 at r0=60 (bottom) does NOT move position but DOES set facing to D;
    #   the 0-edge lands on row 63 (hidden by counter), so visible rows show all 'e' [E100].
    #   Symmetric guess for ACTION1 at r0=0 marked "?" (no evidence yet).
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 is a boundary counter: cols 0..k are '7', cols k+1..63 are '4'. Leftmost '4' at c=k+1.
    #   All-'7' means counter fully right (k=63) [E83,E84,E86].
    # - Counter advances left by 1 on a successful move (1/2/3/4) ONLY when the player's position
    #   actually CHANGES (r0,c0 differ) AND nr0 >= 16 AND nr0 % 20 in {0, 8} [E95,E96,E97,E99].
    #   No advance when position unchanged (E100: ACTION2 at r0=60 stays r0=60) [E100].
    #   No advance when nr0 in {16,24,56} [E88,E90,E97].
    # - Counter does NOT move on ACTION5 when r0 != 12 [E51,E53,E58,E70].
    # - Counter advances left by 1 on ACTION5 at topmost r0==12 every 3rd such press [E72,E74,E76,E78,E80].
    # - After RESET, the FIRST successful move does NOT advance the counter
    #   (one-shot "reset lock" consumed by first successful move) [E83,E84,E86].
    # - When counter reaches col 0, next advance triggers GAME_OVER [E82].
    # - RESET restores level-1 initial layout: player at r48-51 c32-35 facing up, static 4/9 blocks
    #   at r28-31 c16-19 and r36-39 c32-35, r40-43 c32-35 = '1', row63 all '7' [E83,E84,E86].
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
        for r0 in range(0, 61, 4):
            for c0 in range(0, 61, 4):
                n = 0
                for k in range(4):
                    for j in range(4):
                        v = grid[r0+k][c0+j]
                        if v in ("0", "e"):
                            n += 1
                if n > bestn:
                    bestn = n; best = (r0, c0)
        if best is None or bestn <= 0:
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
        if r0 < 0 or r0 > 60 or c0 < 0 or c0 > 60:
            return False
        for k in range(4):
            for j in range(4):
                rr = r0+k
                if rr == 63:
                    continue
                if grid[rr][c0+j] != "1":
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

    def draw_player(r0, c0, facing):
        band = make_band(facing)
        for k in range(4):
            for j in range(4):
                rr = r0+k
                if rr == 63:
                    continue
                grid[rr][c0+j] = band[k][j]

    def erase_player(r0, c0):
        for k in range(4):
            for j in range(4):
                rr = r0+k
                if rr == 63:
                    continue
                grid[rr][c0+j] = "1"

    def build_initial():
        g = [["1"]*64 for _ in range(64)]
        def block4(r0, c0):
            for k in range(4):
                for j in range(4):
                    g[r0+k][c0+j] = "4"
            g[r0+1][c0+1] = "9"; g[r0+1][c0+2] = "9"
            g[r0+2][c0+1] = "9"; g[r0+2][c0+2] = "9"
        block4(28, 16)
        block4(36, 32)
        for k in range(4):
            for j in range(4):
                g[48+k][32+j] = "e"
        for j in range(4):
            g[48][32+j] = "0"
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
            counter_col = 64

    top_press_count = 0
    for h in history:
        if h == "ACTION5":
            top_press_count += 1

    reset_lock = False
    if history and history[-1] == "RESET":
        reset_lock = True

    def counter_advances(nr0):
        if nr0 < 16:
            return False
        m = nr0 % 20
        return m == 0 or m == 8

    game_over = False
    steps = []
    for a in actions:
        if grid is None:
            steps.append({"changes": {}, "levels": 0, "state": "NOT_FINISHED"})
            continue
        if game_over:
            if a == "RESET":
                before = [row[:] for row in grid]
                grid = build_initial()
                counter_col = 64
                top_press_count = 0
                reset_lock = True
                game_over = False
                steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
            else:
                steps.append({"changes": {}, "levels": 0, "state": "GAME_OVER"})
            continue
        before = [row[:] for row in grid]
        counter_moves = False

        if a == "RESET":
            grid = build_initial()
            counter_col = 64
            top_press_count = 0
            reset_lock = True
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
                moved = False
                if 0 <= nr0 <= 60 and 0 <= nc0 <= 60 and region_empty(nr0, nc0):
                    erase_player(r0, c0)
                    draw_player(nr0, nc0, nf)
                    moved = True
                elif a == "ACTION2" and r0 == 60:
                    # bottom edge: position stays, facing becomes D (0-edge hidden on row 63)
                    erase_player(r0, c0)
                    draw_player(r0, c0, "D")
                    moved = False
                elif a == "ACTION1" and r0 == 0:
                    # "?" symmetric guess: position stays, facing becomes U
                    erase_player(r0, c0)
                    draw_player(r0, c0, "U")
                    moved = False
                if moved:
                    if reset_lock:
                        reset_lock = False
                    else:
                        if counter_advances(nr0):
                            counter_moves = True
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

        if counter_moves and counter_col is not None:
            if counter_col > 0:
                grid[63][counter_col - 1] = "4"
                counter_col -= 1
            else:
                game_over = True

        steps.append({"changes": snap(before), "levels": 0, "state": "GAME_OVER" if game_over else "NOT_FINISHED"})
    return {"steps": steps}
