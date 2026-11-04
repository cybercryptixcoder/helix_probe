def predict(probe):
    # Beliefs (v21):
    # - Player is a 4x4 block with 0s on its facing edge, e elsewhere [E1-E60].
    # - ACTION1/2/3/4 move player 4 cells up/down/left/right; blocked if target 4x4 not all '1' [E1-E60].
    # - ACTION5 toggles the lowest uniform-0/3 block in the player's column band between 0 and 3 [E10-E44].
    # - Row 63 is a boundary counter: cols 0..k are '7', cols k+1..63 are '4'. Leftmost '4' at c=k+1.
    #   Moving boundary LEFT by one: c=k+1 becomes '4' [E64,E66].
    # - Counter advances left by 1 on successful ACTION1 when resulting r0 >= 20 [E46,E48,E62,E64,E66,E67].
    #   Does NOT move on ACTION1 when resulting r0 < 20 [E50,E60,E68,E71].
    # - Counter does NOT move on ACTION2/3/4 [E42,E52,E54,E55,E57,E59].
    # - Counter does NOT move on ACTION5 when r0 != 12 [E51,E53,E58,E70].
    # - Counter advances left by 1 on ACTION5 when player is at topmost r0==12 [E72,E74,E76,E78,E80].
    #   BUT: ACTION5 at top advances only on SOME actions, not every one [E74,E76,E78,E80].
    #   Pattern from E74 (after=169, counter at 9): steps 1,2,3 -> no,advance,no.
    #   E76 (after=173, counter at 9): steps 1-4 -> advance,no,no,advance.
    #   E78 (after=178, counter at 7): steps 1-8 -> no,advance,no,no,advance,no,no,advance.
    #   E80 (after=187, counter at 5): steps 1-6 -> no,no,advance,no,no,advance.
    #   The advance pattern is periodic with period 3: advance on every 3rd ACTION5 at top.
    #   ? The phase depends on a hidden counter (total ACTION5-at-top count mod 3).
    #   From E78: advances at steps 2,5,8 (i.e. step%3==2). From E80: advances at steps 3,6 (step%3==0).
    #   From E76: advances at steps 1,4 (step%3==1). From E74: advance at step 2 (step%3==2).
    #   So phase varies; must track a hidden counter of ACTION5-at-top presses.
    #   Let's define: a hidden counter H increments each ACTION5-at-top; advance when H%3==0.
    #   E74 after=169: H starts at some value. steps 1,2,3 -> advance at step2 means H=169+2=171, 171%3=0. 
    #   So H = total ACTION5-at-top presses so far. Advance when (H)%3==0.
    #   Check E76 after=173: step1 H=174 (174%3=0 advance), step2 H=175 no, step3 H=176 no, step4 H=177 (177%3=0 advance). Matches!
    #   Check E78 after=178: step1 H=179 no, step2 H=180 advance, step3 H=181 no, step4 H=182 no, step5 H=183 advance, step6 H=184 no, step7 H=185 no, step8 H=186 advance. Matches!
    #   Check E80 after=187: step1 H=188 no, step2 H=189 advance? But observed step2 no, step3 advance. Hmm.
    #   Wait E80 observed: no,no,advance,no,no,advance. So advance at steps 3,6. H=187+3=190, 190%3=1. Not 0.
    #   Let me recheck. Maybe H counts differently. Let me recount E80: after=187 means 187 actions since level began.
    #   Actually "after" is actions used so far. Hmm, but the phase must be consistent.
    #   E74 after=169, advance at step 2 -> 171. E76 after=173, advance at step 1 -> 174, step4->177.
    #   E78 after=178, advance at step 2 -> 180, step5->183, step8->186.
    #   E80 after=187, advance at step 3 -> 190, step6->193.
    #   171,174,177,180,183,186,190,193: differences 3,3,3,3,3,4,3. 186->190 is 4, inconsistent.
    #   Hmm. Maybe not all actions count, or "after" isn't the counter.
    #   Alternative: maybe advance happens when a separate counter mod 3 == 0, and that counter increments on every action (not just ACTION5-at-top).
    #   E74 after=169: actions at positions 170,171,172. advance at 171 (171%3=0). 
    #   E76 after=173: positions 174,175,176,177. advance at 174(174%3=0),177(177%3=0). Matches!
    #   E78 after=178: positions 179..186. advance at 180,183,186 (all %3==0). Matches!
    #   E80 after=187: positions 188..193. advance at 189(189%3=0),192(192%3=0). But observed advance at steps 3,6 = positions 190,193. 190%3=1, 193%3=1. Doesn't match.
    #   Hmm. Let me recheck E80 observed: [no,no,advance(c3),no,no,advance(c2)]. Steps 3 and 6.
    #   Positions 187+3=190, 187+6=193. Both %3=1.
    #   E74: after=169, advance at step2 -> position 171, %3=0.
    #   These are inconsistent for a global action counter.
    #   Let me reconsider. Maybe the counter advances based on something else entirely.
    #   Actually maybe it's not periodic at all in a simple way, or my position counting is off.
    #   Let me just model: advance on ACTION5-at-top with probability-like pattern... no.
    #   Let me look again: E74 counter went 9->8 at step2. E76 counter 9->8 at step1, 8->7 at step4.
    #   E78 counter 7->6 at step2, 6->5 at step5, 5->4 at step8.
    #   E80 counter 5->4 at step3, 4->3 at step6.
    #   Wait E78 ended at counter 4 (c4). E80 after=187, starts at counter 4? But E80 first advance is at step3 to c3.
    #   E78: after=178, 8 actions, ends after=186. counter went 7->4 (3 advances in 8 actions).
    #   E80: after=187, starts counter at 4 (c4 is leftmost 4). advances to c3 at step3, c2 at step6.
    #   So E80: positions 190,193. E78: positions 180,183,186.
    #   Differences within E78: 3,3. E80: 3. Between E78 last (186) and E80 first (190): 4.
    #   Hmm, gap of 4. Maybe there's an off-by-something. Or maybe the counter advances every 3rd ACTION5-at-top but the count resets or has a different origin.
    #   Actually maybe simpler: advance every 3rd ACTION5-at-top press, tracked as a hidden counter that increments on each ACTION5-at-top, advance when counter%3==0, but the counter's starting value differs.
    #   E74: 3 presses, advance at press 2. So counter before=1 (press1->2 no, press2->3 advance, press3->4 no). counter%3==0 at press2.
    #   E76: 4 presses, advance at press1,4. counter before=2 (press1->3 advance, press2->4, press3->5, press4->6 advance). 
    #   E78: 8 presses, advance at press2,5,8. counter before=1 (press1->2, press2->3 adv, press3->4, press4->5, press5->6 adv, press6->7, press7->8, press8->9 adv).
    #   E80: 6 presses, advance at press3,6. counter before=0 (press1->1, press2->2, press3->3 adv, press4->4, press5->5, press6->6 adv).
    #   So starting counter: E74=1, E76=2, E78=1, E80=0. These must be consistent with total ACTION5-at-top presses before each experiment.
    #   This is getting complex. Given uncertainty, I'll model it as: advance every 3rd ACTION5-at-top press using a hidden counter that I track by replaying history.
    #   But I don't have reliable history. Simplest robust guess: advance on ACTION5-at-top roughly every 3rd, but I'll just predict advance on every ACTION5-at-top (over-predict) OR use a mod-3 on a replayed counter.
    #   Given the goal is to reach col 0, and it's slow, let me just predict advance on every ACTION5-at-top (v20 did this and got 0.58-0.83). Actually the truth is ~1/3 rate.
    #   Better: track a hidden counter by replaying history. The history is available in probe["history"].
    #   I'll count ACTION5-at-top presses in history and use mod 3. But I need to know the phase.
    #   Given the data, let me just use: advance when (count of ACTION5-at-top presses so far in this level) % 3 == 0, where count includes current. But phase unclear.
    #   I'll go with: maintain hidden counter, advance when counter%3==0, increment counter each ACTION5-at-top. Initialize from history.
    #   Since I can't determine exact phase, I'll guess counter starts at 0 and advance when counter%3==0 AFTER increment (i.e. press1->1 no, press2->2 no, press3->3 yes).
    #   This matches E80 (advance at press3,6). For others it may be off by phase but it's the best guess.
    # - Goal: ? Best guess: shift boundary all the way left (counter reaches col 0) via counter advances.
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

    counter_col = None
    if grid is not None:
        row63 = grid[63]
        for c in range(64):
            if row63[c] == "4":
                counter_col = c
                break

    # Hidden counter for ACTION5-at-top advance phase.
    # Replay history to count ACTION5-at-top presses. We can't know player pos from history alone,
    # so approximate: count all ACTION5 in history as potential top presses (best guess).
    # ? phase: advance when press_count % 3 == 0 (after increment).
    top_press_count = 0
    for h in history:
        if h == "ACTION5":
            top_press_count += 1

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
                    if a == "ACTION1" and nr0 >= 20:
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

        if counter_col is not None and counter_col > 0 and counter_moves:
            grid[63][counter_col - 1] = "4"
            counter_col -= 1

        steps.append({"changes": snap(before), "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
