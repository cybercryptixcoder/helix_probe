def predict(probe):
    # Beliefs (v27):
    # - Player is a 4x4 block with 0s on its facing edge, e elsewhere [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1' [E1-E60].
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 is a boundary counter: cols 0..k are '7', cols k+1..63 are '4'. Leftmost '4' at c=k+1.
    #   All-'7' means counter fully right (k=63, no '4' visible) [E83,E84,E86].
    # - Counter advances left by 1 on successful ACTION1 when resulting nr0 >= 16 and nr0 % 20 != 0
    #   [E46,E48,E62,E64,E66,E67,E85,E93]. Does NOT advance when nr0 < 16 [E88] or nr0 % 20 == 0 [E85,E90,E93].
    # - Counter does NOT move on ACTION2/3/4 [E42,E52,E54,E55,E57,E59,E84].
    # - Counter does NOT move on ACTION5 when r0 != 12 [E51,E53,E58,E70].
    # - Counter advances left by 1 on ACTION5 at topmost r0==12 every 3rd such press [E72,E74,E76,E78,E80].
    # - After RESET, the FIRST successful move does NOT advance the counter
    #   (a one-shot "reset lock" flag consumed by the first successful move, regardless of direction) [E83,E84,E86].
    # - When counter reaches col 0 (all-'7' with a '4' at c0), the next advance triggers GAME_OVER [E82].
    # - RESET restores level-1 initial layout: player at r48-51 c32-35 facing up, static 4/9 blocks
    #   at r28-31 c16-19 and r36-39 c32-35, r40-43 c32-35 = '1', row63 all '7' [E83,E84,E86].
    # - Goal: ? Best guess: shift boundary all the way left (counter reaches col 0) via advances.
    #
    # v27 fixes (E99, E95, E96, E97, E98):
    # - The player is NOT a 4x4 block with a facing edge; it is a 1-cell-wide "lane" block of width 4
    #   whose shape is [e,e,e,0] etc. Actually: the moving object is a 4x4 block whose bottom row is
    #   [e,e,e,0] (facing D) or top row [0,e,e,e] (facing U) etc. The player occupies 4x4 but only
    #   ONE row/col is the "0 edge"; the rest is 'e'. On movement the WHOLE 4x4 moves.
    # - E99: after ACTION2 the player moved DOWN but only 3 rows of 'e' appeared (r60-62), not 4,
    #   because the 4th row (r63) is the counter row. So the player's 4x4 can overlap row 63; the
    #   counter row is drawn on top / the player's bottom row at r63 is hidden. Actually observed:
    #   ACTION2 moved player from r56-59 to r60-63, but only r60-62 show 'e' (r63 keeps counter).
    #   So player CAN move to r0=60 (bottom at 63) and its bottom row is overwritten by counter.
    # - E99 ACTION3: player moved LEFT from c24-27 to c20-23, but only 3 columns of 'e' (c21-23),
    #   because c20 is the '0' edge column. Wait: observed r60 c20:0, c21-23:e. So the 0-edge is on
    #   the LEFT (facing L) after ACTION3. And rows r60-62 only (r63 is counter). Consistent.
    # - E95: ACTION3 from facing-up player: player moves left, becomes facing L, 0-edge on left col.
    #   Observed r40 c28:0, c29-31:e — yes 0 on left. And counter advanced (c62:4) — ACTION3 DID
    #   advance counter here! But E42 said ACTION3 doesn't move counter. Difference: in E95 the
    #   player was at r0=40 (nr0=40, 40%20==0). Hmm, but counter advanced. Let me re-check E42.
    #   Actually in E95 counter went from c63 to c62 (advanced 1). So ACTION3 CAN advance counter.
    #   Re-examine: maybe counter advances on ANY successful move when resulting position satisfies
    #   a modular condition, not just ACTION1. E96 ACTION2 at r0=12->...->r0=52 advanced counter
    #   (c61:4 after 3rd ACTION2, nr0=52, 52%20!=0, >=16). E97 ACTION2 to r0=60 advanced (c60:4).
    #   E99 ACTION3 advanced (c58:4). So: counter advances on ANY successful move (1/2/3/4) when
    #   resulting nr0 >= 16 and nr0 % 20 != 0. But E42 ACTION3/4 didn't advance — because there
    #   nr0 was probably <16 or %20==0. Let me adopt: counter advances on successful ACTION1/2/3/4
    #   when nr0 >= 16 and nr0 % 20 != 0. (nr0 = resulting row of player top.)
    #   Check E54 ACTION2 no advance: nr0 likely <16 or %20==0. E52 ACTION4/3 no advance: same.
    #   This unifies the rule. [E95,E96,E97,E99 support; E42,E52,E54 consistent if nr0 condition]
    # - E98: ACTION5 at r0=12 (topmost) advanced counter on 3rd press (c59:4). Consistent with
    #   every-3rd-press rule. Good.
    # - E97: ACTION2 to r0=60 (bottom at 63): counter advanced c60:4. Then ACTION1 back up to
    #   r0=56: counter did NOT advance (nr0=56, 56%20!=0, >=16 — should advance!). But observed
    #   no counter change on that ACTION1. Hmm. Wait E97 last step: ACTION1 from r0=60 to r0=56,
    #   observed r56 c24-27:0 (0 on top = facing U), no counter change. nr0=56, 56>=16, 56%20=16!=0.
    #   So why no advance? Maybe because player was at bottom (r0=60) — moving up from the very
    #   bottom row doesn't advance? Or: the counter advances only when the player's bottom row
    #   (nr0+3) is < 63? At r0=56, bottom=59<63, should be fine. Contradiction.
    #   Alternative: counter advances when nr0 % 20 == 16? 56%20=16 yes. 52%20=12 no but E96 advanced.
    #   Hmm E96: r0 went 12->16->20->24? No wait E96 started after=5, three ACTION2: 12->16->20->24?
    #   Observed r40->r44->r48->r52. So r0: 36->40->44->48->52? After=5 means player was at r36.
    #   ACTION2: 36->40 (no adv, 40%20==0), 40->44 (no adv? 44>=16,44%20=4!=0 should adv but didn't),
    #   44->48 (adv? observed c61:4 on 3rd step, so 48 advanced). Hmm 44 didn't but 48 did.
    #   Maybe condition is nr0 % 20 == 8? 48%20=8 yes. 52%20=12 no. But E97 60%20=0 no adv... 
    #   This is getting complex. Let me use: advance when nr0 in {48,52,56,...}? 
    #   E96: 48 advanced (c61). E97: 60 advanced (c60). E99: 60 advanced (c58). E95: 40 advanced (c62).
    #   E88: r0=12->16, no advance (16). E90: r0=20->24, no advance (24). 
    #   So advanced at nr0: 40(E95), 48(E96), 60(E97), 60(E99). Not at: 16(E88), 24(E90), 56(E97).
    #   Pattern: advance when nr0 % 20 in {0}? 40%20=0 yes, 60%20=0 yes, 48%20=8 no but advanced.
    #   Hmm 48 advanced. 56 didn't. 48%16=0, 56%16=8. 40%16=8. 60%16=12. No clean pattern.
    #   Let me try: advance when nr0 is a multiple of 4 AND (nr0//4) is odd? 40/4=10 even no. 
    #   Try nr0 in {40,48,60} advanced, {16,24,56} not. 40=8*5,48=8*6,60=8*7.5 no.
    #   Honestly the cleanest: advance when nr0 >= 16 and nr0 % 20 == 0 OR nr0 % 20 == 8? 
    #   40%20=0 yes, 48%20=8 yes, 60%20=0 yes, 16%20=16 no, 24%20=4 no, 56%20=16 no. 
    #   That fits all! Rule: advance when nr0>=16 and (nr0%20==0 or nr0%20==8).
    #   But E46/E48/E62 etc said ACTION1 advances at various nr0. Let me just use this heuristic
    #   and mark "?".
    # - Also E97 ACTION2 to r0=60: player bottom at 63, counter row overwritten. The 'e' only shows
    #   r60-62. And counter advanced. So player can sit at r0=60.
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
        # find 4x4 region containing '0' and 'e' cells (the player)
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
                    continue  # counter row, ignore
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
        # "?" heuristic: advance when nr0>=16 and (nr0%20==0 or nr0%20==8)
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
                if 0 <= nr0 <= 60 and 0 <= nc0 <= 60 and region_empty(nr0, nc0):
                    for k in range(4):
                        for j in range(4):
                            rr = r0+k
                            if rr == 63:
                                continue
                            grid[rr][c0+j] = "1"
                    band = make_band(nf)
                    for k in range(4):
                        for j in range(4):
                            rr = nr0+k
                            if rr == 63:
                                continue
                            grid[rr][nc0+j] = band[k][j]
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
