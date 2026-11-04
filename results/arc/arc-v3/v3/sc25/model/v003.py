def predict(probe):
    # Model v3 — mechanism from E1-E4.
    #
    # Screen layout (level 1):
    #  - Top-right counter: rows 0..17 at cols 62-63. Each "advance" fills the
    #    next 2-row band (r=2k,2k+1) with 0. Bands fill in order 0,2,4,...,16.
    #    [E1 r0-1; E2 r2-3; E2 r4-5; E3 r6-7; E3 r8-9; E4 r10-11,r12-13,
    #     r14-15,r16-17]
    #  - The 4x4 "puzzle" block at rows 19-22, cols 35-42. ACTION2 and ACTION4
    #    rotate/shift its 2x2 sub-tiles. ACTION2: swaps the two 2x2 halves
    #    horizontally (left<->right). ACTION4: swaps vertically (top<->bottom).
    #    [E1 ACTION2; E2 ACTION1/ACTION3/ACTION4; E4 ACTION2,ACTION4]
    #    Actually ACTION1/ACTION3 also change it (E2). Model as a cyclic shift.
    #  - Target blocks at rows 49-51 (cols 29-31) and rows 59-61 (cols 29-31 or
    #    34-36). CLICK at x=30 lights the c29-31 block; x=35 lights c34-36.
    #    A click toggles: first click sets to 0 (off), second sets to e (on)?
    #    [E1 CLICK30 50 -> r49-51 c29-31:e; E3 CLICK35 60 -> r59-61 c34-36:e;
    #     E3 CLICK30 60 -> r59-61 c29-31:e; E4 CLICK30 50 -> r49-51 c29-31:0,
    #     then again -> :e].  So repeated click toggles 0<->e.
    #
    # Which actions advance the counter?  From evidence:
    #   E1: CLICK30 50 advanced (r0-1). CLICK35 50 did NOT (first action, 0 chg).
    #   E2: ACTION1 -> r2-3 (advance); ACTION1 -> nothing; ACTION3 -> r4-5;
    #       ACTION4 -> nothing.
    #   E3: CLICK35 60 -> r6-7; CLICK15 20 -> nothing; CLICK30 60 -> r8-9;
    #       CLICK63 3 -> nothing.
    #   E4: ACTION2 -> nothing; ACTION4 -> r10-11; CLICK30 50 -> r12-13;
    #       CLICK30 50 -> nothing(counter); ACTION1 -> r14-15; ACTION1 -> nothing;
    #       ACTION1 -> r16-17.
    # Pattern: the counter advances on alternating "advance-capable" actions.
    #   Advance-capable set = {ACTION1, ACTION3, ACTION4, CLICK x in {30,35}}.
    #   ACTION2 is NOT advance-capable. Clicks at other x are not.
    #   It advances only every OTHER such action (a toggle/parity).
    #   Check E4: ACTION2(no), ACTION4(adv r10), CLICK30(adv r12), CLICK30(no),
    #     ACTION1(adv r14), ACTION1(no), ACTION1(adv r16). Yes: alternating.
    #   Check E2: ACTION1(adv r2), ACTION1(no), ACTION3(adv r4), ACTION4(no).
    #     Yes alternating.
    #   Check E1: CLICK35 50 (adv-capable, but first -> no adv? observed 0 chg),
    #     ACTION2 (not capable), CLICK16 55 (not), CLICK30 50 (adv r0).
    #     Hmm: with parity, CLICK35 50 would be the 1st capable -> should advance.
    #     But it didn't. So maybe parity starts such that first capable does NOT
    #     advance. Then E1: CLICK35(no), CLICK30(adv r0) — consistent if the
    #     "no-advance" phase is first. But E2 first ACTION1 DID advance...
    #     E2 started after E1 (4 actions). E1 ended with CLICK30 advancing.
    #     So parity carries across probes via history. Good — model parity by
    #     replaying history.
    #   Let's define: each advance-capable action flips a parity bit; counter
    #   advances when parity flips to "advance" state. Determine initial phase
    #   from history.
    #
    # ? Goal guess: fill all counter bands (rows 0-17 -> 0) i.e. 9 advances,
    #   OR light the correct target. Unproven. We predict counter advances and
    #   target toggles; levels stays 0 unless counter fully filled (guess).

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", []) or []

    def count_bands(fr):
        if not fr:
            return 0
        n = 0
        for k in range(9):
            r = 2 * k
            if r < len(fr) and len(fr[r]) > 63 and fr[r][62] == '0' and fr[r][63] == '0':
                n += 1
            else:
                break
        return n

    def is_adv_capable(a):
        if not isinstance(a, str):
            return False
        if a in ("ACTION1", "ACTION3", "ACTION4"):
            return True
        if a.startswith("CLICK"):
            try:
                p = a.split()
                x = int(p[1])
                return x in (30, 35)
            except Exception:
                return False
        return False

    # Replay history to get current parity and band count.
    # parity: number of advance-capable actions seen so far (mod 2).
    # We need to know whether the NEXT capable action advances.
    # From E1: first capable (CLICK35 50) did NOT advance. So parity 0 -> no adv,
    # parity 1 -> advance, then flip. i.e. advance when (count % 2 == 1).
    # Verify E2: after E1, count of capable in E1 = 2 (CLICK35, CLICK30).
    #   E2 ACTION1: count becomes 3 -> odd -> advance (r2-3). Yes!
    #   E2 ACTION1: count 4 -> even -> no. Yes.
    #   E2 ACTION3: count 5 -> odd -> advance (r4-5). Yes.
    #   E2 ACTION4: count 6 -> even -> no. Yes.
    # Verify E3: after E2, capable count = 2+2 = 4.
    #   E3 CLICK35 60: count 5 -> odd -> advance (r6-7). Yes.
    #   E3 CLICK15 20: not capable, count stays 5.
    #   E3 CLICK30 60: count 6 -> even -> NO advance?? But observed r8-9!
    #   Contradiction. Hmm.
    # Let's recount. E1 capable: CLICK35 50, CLICK30 50 = 2. 
    # E2 capable: ACTION1,ACTION1,ACTION3,ACTION4 = 4. total 6.
    # E3: CLICK35 60 -> count 7 odd -> advance r6-7 (yes).
    #     CLICK15 20 -> not capable.
    #     CLICK30 60 -> count 8 even -> should NOT advance, but it DID (r8-9).
    # So parity model fails. 
    #
    # Alternative: maybe it's not parity but "advance unless the previous
    # advance-capable action already advanced and no non-capable action between"?
    # Look: consecutive capable actions: E2 ACTION1(adv),ACTION1(no),ACTION3(adv),
    #   ACTION4(no). E4 ACTION4(adv),CLICK30(adv),CLICK30(no),ACTION1(adv),
    #   ACTION1(no),ACTION1(adv). 
    # E4: ACTION4 adv, then CLICK30 adv (two in a row advanced!). So not simple
    #   alternation either.
    # Hmm E4: ACTION2(no, not capable), ACTION4(adv r10), CLICK30(adv r12),
    #   CLICK30(no), ACTION1(adv r14), ACTION1(no), ACTION1(adv r16).
    # So sequence of capable actions in E4: ACTION4(adv),CLICK30(adv),CLICK30(no),
    #   ACTION1(adv),ACTION1(no),ACTION1(adv). Pattern: adv,adv,no,adv,no,adv.
    # E2 capable: ACTION1(adv),ACTION1(no),ACTION3(adv),ACTION4(no): adv,no,adv,no.
    # E1 capable: CLICK35(no),CLICK30(adv): no,adv.
    # E3 capable: CLICK35(adv),CLICK30(adv): adv,adv.
    # Concatenate all capable actions across history in order:
    #   E1: CLICK35(no), CLICK30(adv)
    #   E2: A1(adv), A1(no), A3(adv), A4(no)
    #   E3: C35(adv), C30(adv)
    #   E4: A4(adv), C30(adv), C30(no), A1(adv), A1(no), A1(adv)
    # Full sequence of adv/no: no,adv, adv,no,adv,no, adv,adv, adv,adv,no,adv,no,adv
    # Hmm irregular. Let me look for a different rule.
    #
    # Maybe the counter advances based on the ACTION TYPE cycling, not parity.
    # Actually maybe each action has a fixed effect but the counter only advances
    # when the puzzle block is in a certain configuration? Unlikely.
    #
    # Simpler: maybe the counter advances on a fixed subset and my reading of
    # "which actions" is wrong. Let me just tabulate per action:
    #   ACTION1: E2 adv, E2 no, E4 adv, E4 no, E4 adv. -> mixed.
    #   ACTION3: E2 adv. 
    #   ACTION4: E2 no, E4 adv.
    #   CLICK30: E1 adv, E3 adv, E4 adv, E4 no.
    #   CLICK35: E1 no, E3 adv.
    # Mixed everywhere -> there IS hidden state (parity/counter).
    #
    # Given difficulty, model: counter advances on advance-capable actions with
    # a parity that flips each capable action, BUT the observed data doesn't fit
    # a single global parity. Best guess: advance when (capable_count is odd)
    # for CLICKs, and ACTION1/3/4 advance on their own sub-parity. Too complex.
    #
    # Pragmatic model: predict counter advances on every advance-capable action
    # EXCEPT when the immediately preceding action was also advance-capable and
    # advanced (i.e. no two consecutive advances). Check:
    #   E1: C35(prev none -> adv? but observed no). Fails at start.
    #
    # I'll go with: replay history, maintain a toggle that flips on each
    # advance-capable action; advance when toggle becomes True, starting False.
    # This matches E1(no,adv),E2(adv,no,adv,no),E3(adv,no? but observed adv,adv).
    # E3 fails. 
    #
    # Given the mess, I'll model the counter as advancing on advance-capable
    # actions with parity, and accept imperfection. Use parity: advance when
    # capable_count (before this action) is even -> i.e. 1st capable no, 2nd yes,
    # 3rd no... Check E1: C35 count0 even->no (yes), C30 count1 odd->? 
    # Let me define advance when count%2==0 (0-indexed even -> advance). 
    #   E1 C35: count0 -> adv? observed no. So advance when count%2==1.
    #   E1 C35 count0 -> no (ok), C30 count1 -> adv (ok).
    #   E2 A1 count2 -> no? observed adv. Fails.
    #
    # I cannot find a clean global rule. I'll use the simplest that fits most:
    # advance on advance-capable action when the PREVIOUS action (any) was not
    # advance-capable OR ... no.
    #
    # Decision: model counter advance on advance-capable actions using a
    # per-action-type rule derived from majority:
    #   CLICK30: advances (3/4) -> advance
    #   CLICK35: advances (1/2) -> advance
    #   ACTION1: advances (3/5) -> advance
    #   ACTION3: advances (1/1) -> advance
    #   ACTION4: advances (1/2) -> advance
    # i.e. ALL advance-capable actions advance the counter, except when the
    # counter is already at max. This over-predicts but is simple.
    # Actually E2 A1(no) and E4 A1(no),E4 C30(no) contradict. But majority.
    #
    # I'll add: do not advance if the immediately previous action was the SAME
    # advance-capable action (repeated same action doesn't double-advance).
    #   E2 A1,A1: second no (ok). E4 C30,C30: second no (ok). E4 A1,A1: no(ok).
    #   E4 A1,A1,A1: 1st adv,2nd no,3rd adv -> matches E4 (adv,no,adv)! 
    #   E2 A1(adv),A1(no),A3(adv),A4(no): A3 prev A1 diff -> adv ok; A4 prev A3
    #     diff -> adv? observed no. Fails.
    # Hmm E2 A4 observed no. 
    #
    # OK final pragmatic: advance on advance-capable action unless the previous
    # action was identical. Accept E2 A4 miss.

    # Replay history to get band count and last action.
    bands = count_bands(frame)
    last = history[-1] if history else None

    steps = []
    for a in actions:
        changes = {}
        adv = is_adv_capable(a) and a != last and bands < 9
        if adv:
            r = 2 * bands
            for dr in (0, 1):
                for c in (62, 63):
                    changes["%d,%d" % (r + dr, c)] = '0'
            bands += 1
        # Puzzle block 4x4 at rows 19-22, cols 35-42: rotate tiles.
        # ACTION2: swap left/right 2x2 halves. ACTION4: swap top/bottom halves.
        # ACTION1/ACTION3: shift. Model as changing colours in the block.
        # We don't track exact colours; predict a generic change region.
        # (Leave puzzle-block changes out to avoid wrong cells; the counter and
        #  target are the main signals.)
        # Target toggle on CLICK x in {30,35}.
        if isinstance(a, str) and a.startswith("CLICK"):
            try:
                p = a.split()
                x = int(p[1]); y = int(p[2])
            except Exception:
                x = y = -1
            if x == 30:
                # toggle rows 49-51 c29-31 (and 59-61 c29-31 if y large)
                if y >= 55:
                    for rr in (59, 60, 61):
                        for cc in (29, 30, 31):
                            changes["%d,%d" % (rr, cc)] = 'e'
                else:
                    for rr in (49, 50, 51):
                        for cc in (29, 30, 31):
                            changes["%d,%d" % (rr, cc)] = 'e'
            elif x == 35:
                for rr in (59, 60, 61):
                    for cc in (34, 35, 36):
                        changes["%d,%d" % (rr, cc)] = 'e'
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
        last = a
    return {"steps": steps}
