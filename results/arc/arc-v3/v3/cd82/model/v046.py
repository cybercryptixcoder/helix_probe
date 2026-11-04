def predict(probe):
    # Beliefs (revised v46):
    # - Row 63 is a progress bar filling right-to-left from c63; each accepted action fills one cell.
    # - CLICK: the FIRST click on a given (x,y) cell in the level is inert; every SUBSEQUENT click on that
    #   cell advances the bar by one [E80 N,Y; E48 N,Y; E84 N,Y,~; E86 N,Y,Y; E90 click after actions advances].
    # - ACTION: advances the bar on EVERY use, including repeats and the first action after RESET
    #   [E88: A1,A1,A2,A2 -> advance,no,advance,advance; E90: A2,A2,A2 -> adv,no,adv; E94: A1,A1,A1 -> adv,no,adv].
    #   The pattern is: an ACTION advances UNLESS it is the same as the immediately preceding action
    #   (i.e. "differs from previous action" rule). E94 confirms: A1(adv), A1(same->no), A1(differs from prev A1? no)...
    #   Wait: E94 A1,A1,A1 gave adv,no,adv. So it's NOT "differs from previous". It alternates.
    #   E88 A1,A1,A2,A2 -> adv,no,adv,adv. E90 A2,A2,A2 -> adv,no,adv. E94 A1,A1,A1 -> adv,no,adv.
    #   Pattern: advance on 1st, skip 2nd, advance 3rd... i.e. advance when count of consecutive same action is ODD.
    #   Check E88: A1(1st,odd->adv),A1(2nd,even->no),A2(1st,odd->adv),A2(2nd,even->no) but observed adv,no,adv,adv.
    #   Hmm E88 last A2 advanced. So not simple parity.
    #   Re-examine: E88 A1,A1,A2,A2 -> adv,no,adv,adv. E90 A2,A2,A2 -> adv,no,adv. E94 A1,A1,A1 -> adv,no,adv.
    #   E87 A2,A1 -> no,adv (A2 first inert? but E90 A2 first advanced). E87 was mid-level though.
    #   Best fit: ACTION advances unless it equals the previous action AND that previous action also advanced?
    #   Simpler: track "last action that advanced". An ACTION advances if it differs from the last ADVANCING action.
    #   E88: A1 adv(last=A1), A1 same->no, A2 diff->adv(last=A2), A2 same->no... but observed adv. Contradiction.
    #   Try: advance unless same as immediately previous action, EXCEPT the rule resets... 
    #   Given E88 adv,no,adv,adv and E90 adv,no,adv and E94 adv,no,adv: 
    #   the 2nd of a pair is skipped, but a NEW action type always advances, and a 3rd repeat advances again.
    #   Model: count consecutive identical actions; advance if count is odd OR it's a new action type.
    #   E88: A1#1 odd adv, A1#2 even no, A2#1 new adv, A2#2 even... but observed adv. Fails.
    #   Alternative: advance if action != previous action OR previous action did NOT advance.
    #   E88: A1 adv(prev none). A1: same as prev, prev advanced -> no. A2: diff -> adv. A2: same, prev advanced -> no. Observed adv. Fails.
    #   Let me just use: ACTION advances unless it is the 2nd consecutive identical action (count==2 mod 2 ==0 but only skip exactly the 2nd).
    #   E88: A1#1 adv, A1#2 no, A2#1 adv, A2#2 no -> but observed adv. Still fails on last.
    #   Given difficulty, use best simple rule: advance unless same as previous action, but this fails E88/E90/E94 3rd.
    #   I'll adopt: advance if action differs from previous action, OR if it's the 3rd+ in a run (count>=3 odd).
    #   E88: A1#1 adv, A1#2 no, A2#1 adv, A2#2 no -> observed adv. Fails.
    #   Honestly the cleanest fit across E88,E90,E94: advance on odd-numbered occurrences within a run.
    #   E88 A1#1 adv, A1#2 no, A2#1 adv, A2#2 no. Observed: adv,no,adv,adv. Only last differs.
    #   E90 A2#1 adv, A2#2 no, A2#3 adv. Matches odd rule.
    #   E94 A1#1 adv, A1#2 no, A1#3 adv. Matches odd rule.
    #   E88 is the outlier on the 4th. Possibly E88's 4th A2 advanced because... prior CLICK? No clicks there.
    #   I'll go with odd-run rule and accept E88 mismatch.
    # - RESET clears row 63 back to '4' [E30,E66,E70,E92,E94]
    # - When bar is full (64 cells) -> GAME_OVER [E30]
    # - GOAL "?": completing level 1 is NOT filling the bar (that gives GAME_OVER). Likely requires
    #   arranging the r7 switch/objects; unproven. Marked "?" below.
    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)
    history = probe.get("history", []) or []
    grid = [list(row) for row in frame] if frame else [['5']*64 for _ in range(64)]

    def bar_fill(g):
        n = 0
        for c in range(63, -1, -1):
            if g[63][c] == '5':
                n += 1
            else:
                break
        return n

    def clear_bar(g, ch):
        for c in range(64):
            if g[63][c] != '4':
                ch["63,%d" % c] = '4'
                g[63][c] = '4'

    # replay history to recover per-cell click counts and action-run state
    counts = {}
    run_act = None
    run_len = 0
    for h in history:
        h = h.strip()
        if h == "RESET":
            counts = {}
            run_act = None
            run_len = 0
        elif h.startswith("CLICK"):
            p = h.split()
            try:
                t = (int(p[1]), int(p[2]))
            except Exception:
                t = None
            if t:
                counts[t] = counts.get(t, 0) + 1
            run_act = None
            run_len = 0
        elif h.startswith("ACTION"):
            if h == run_act:
                run_len += 1
            else:
                run_act = h
                run_len = 1

    steps = []
    state = "NOT_FINISHED"
    levels = level

    def advance(g, ch):
        fill = bar_fill(g)
        if fill < 64:
            col = 63 - fill
            if g[63][col] != '5':
                ch["63,%d" % col] = '5'
                g[63][col] = '5'
                return True
        return False

    for act in actions:
        ch = {}
        act = act.strip()
        if state == "GAME_OVER":
            if act == "RESET":
                clear_bar(grid, ch)
                state = "NOT_FINISHED"
                counts = {}
                run_act = None
                run_len = 0
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue
        if act == "RESET":
            clear_bar(grid, ch)
            state = "NOT_FINISHED"
            counts = {}
            run_act = None
            run_len = 0
            steps.append({"changes": ch, "levels": levels, "state": state})
            continue

        if act.startswith("CLICK"):
            p = act.split()
            try:
                x = int(p[1]); y = int(p[2])
            except Exception:
                x = y = -1
            t = (x, y)
            counts[t] = counts.get(t, 0) + 1
            if counts[t] >= 2:
                advance(grid, ch)
            run_act = None
            run_len = 0
        else:
            if act == run_act:
                run_len += 1
            else:
                run_act = act
                run_len = 1
            # advance on odd-numbered occurrence within a run
            if run_len % 2 == 1:
                advance(grid, ch)

        fill = bar_fill(grid)
        if fill >= 64:
            state = "GAME_OVER"
        steps.append({"changes": ch, "levels": levels, "state": state})
    return {"steps": steps}
