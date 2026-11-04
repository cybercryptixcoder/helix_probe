def predict(probe):
    # Model v4 — mechanism from E1-E5.
    #
    # Screen layout (level 1):
    #  - Top-right counter: rows 0..19 at cols 62-63. Each "advance" fills the
    #    next 2-row band (r=2k,2k+1) with 0. Bands fill in order 0,2,4,...,18.
    #    [E1 r0-1; E2 r2-3,r4-5; E3 r6-7,r8-9; E4 r10-11,r12-13,r14-15,r16-17;
    #     E5 r18-19].  So 10 bands total (rows 0..19).
    #  - The 4x4 "puzzle" block at rows 19-22, cols 35-42. ACTION2 and ACTION4
    #    rotate/shift its 2x2 sub-tiles. ACTION1/ACTION3 also change it.
    #  - Target blocks: a click at x=30 or x=35 lights a 3x3 block at cols
    #    29-31 or 34-36, at a row determined by the click's y (rounded to a
    #    block). E5: CLICK 30 55 -> rows 54-56 c29-31:e. E3: CLICK 30 60 ->
    #    rows 59-61 c29-31:e. E1: CLICK 30 50 -> rows 49-51 c29-31:e.
    #    E4: CLICK 30 50 -> rows 49-51 c29-31:0 then :e (toggle e<->0).
    #    E5 second click -> rows 54-56 c29-31:2 (a THIRD state, colour 2).
    #    So repeated clicks cycle the target through e -> 0 -> 2 -> ...?
    #    Actually E4: e then 0. E5: e then 2. Different! So the state depends
    #    on history (which target / how many times lit).
    #
    # Counter advance rule (the key puzzle):
    #   Sequence of advance-capable actions and whether they advanced:
    #   E1: C35(no), C30(adv)
    #   E2: A1(adv), A1(no), A3(adv), A4(no)
    #   E3: C35(adv), C30(adv)
    #   E4: A2(no,not cap), A4(adv), C30(adv), C30(no), A1(adv), A1(no), A1(adv)
    #   E5: C30(adv), C30(no)
    # Look at E5: C30(adv), C30(no) — same action repeated: adv then no.
    # E4 C30,C30: adv then no. E2 A1,A1: adv then no. E4 A1,A1,A1: adv,no,adv.
    # So: repeating the SAME action toggles advance/no. And E4 A4(adv) then
    # C30(adv): different actions, both advanced. E2 A1(adv),A1(no),A3(adv):
    # A3 after A1(no) advanced. E3 C35(adv),C30(adv): different, both adv.
    # E1 C35(no),C30(adv): different, first no second adv.
    #
    # Hypothesis: there is a global toggle T. Each advance-capable action:
    #   if T is "on", advance and set T off; if T off, don't advance and set T on.
    #   i.e. alternate adv/no across ALL capable actions.
    # Check concatenated capable sequence (adv/no):
    #   E1: no,adv
    #   E2: adv,no,adv,no
    #   E3: adv,adv  <-- breaks alternation!
    # Hmm E3 C35(adv),C30(adv) two advs in a row.
    #
    # Alternative: toggle flips only on NON-advance? Or the toggle is per
    # action-type? Let's check per-type:
    #   C30: E1 adv, E3 adv, E4 adv, E4 no, E5 adv, E5 no -> adv,adv,adv,no,adv,no
    #   C35: E1 no, E3 adv -> no,adv
    #   A1: E2 adv,no; E4 adv,no,adv -> adv,no,adv,no,adv
    #   A3: E2 adv
    #   A4: E2 no; E4 adv -> no,adv
    # A1 sequence adv,no,adv,no,adv = perfect alternation starting adv.
    # C30: adv,adv,adv,no,adv,no — not clean.
    # C35: no,adv = alternation starting no.
    # A4: no,adv = alternation starting no.
    # A3: adv.
    #
    # Maybe the toggle is global but E3's two advs are because a non-capable
    # action (CLICK 15 20) between them reset something? E3 order:
    #   C35(adv), CLICK15 20(not cap), C30(adv). If non-capable actions don't
    #   affect toggle, then adv,adv breaks it. Unless CLICK15 20 toggled.
    #
    # Let me try: global toggle flips on EVERY action (capable or not), and
    # advances when toggle is in "adv" phase AND action is capable.
    #   Need to fit. Too many unknowns.
    #
    # Simplest robust model that fits the repeated-same-action pattern:
    #   advance if action is capable AND (previous action != this action).
    # Check:
    #   E1: C35 prev=None -> adv? observed no. (prev None treated as same? no)
    #   E2: A1 prev=C30(diff)->adv ok; A1 prev=A1(same)->no ok; A3 prev=A1(diff)
    #       ->adv ok; A4 prev=A3(diff)->adv? observed no. FAIL.
    #   E3: C35 prev=A4(diff)->adv ok; C30 prev=C15(diff)->adv ok.
    #   E4: A4 prev=A2(diff)->adv ok; C30 prev=A4(diff)->adv ok; C30 prev=C30
    #       (same)->no ok; A1 prev=C30(diff)->adv ok; A1 same->no ok; A1 same->
    #       no? observed adv. FAIL (A1,A1,A1: adv,no,adv).
    # So "same as previous" fails on triple repeats (E4 A1 x3 gives adv,no,adv).
    # That's alternation on repeats: adv,no,adv. So repeated same action
    # alternates. And different action after a "no" gives adv (E2 A3 after A1no).
    # And different action after "adv" gives adv (E4 C30 after A4adv; E3 C30
    # after C35adv).
    #
    # Rule attempt: maintain toggle T (start: adv). On capable action:
    #   if T==adv: advance, T=no. else: no advance, T=adv.
    #   On NON-capable action: leave T unchanged.
    # Check E1: start T=adv. C35: T=adv -> adv? observed NO. So start T=no.
    #   start T=no: C35 -> no, T=adv. C30 -> adv, T=no. matches E1!
    # E2 continues T=no: A1 -> no? observed adv. FAIL.
    #   Unless T carried differently. E1 ended T=no. E2 A1 should be no but is adv.
    #
    # Maybe T flips on EVERY action (capable or not), advance when capable & T=adv.
    #   E1: actions C35,C2,C16,C30. Start T=adv?
    #     C35: T=adv,capable->adv? observed no. start T=no.
    #     C35: T=no -> no, flip T=adv.
    #     C2: not capable, flip T=no.
    #     C16: not capable, flip T=adv.
    #     C30: T=adv,capable->adv ok, flip T=no. E1 matches!
    #   E2: A1,A1,A3,A4. Start T=no.
    #     A1: T=no->no? observed adv. FAIL.
    # Hmm.
    #
    # Let me reconsider: maybe advance depends on the PUZZLE BLOCK state, not
    # a counter. But that's hard.
    #
    # Given time, best pragmatic model: global toggle that flips on each
    # capable action, advance when toggle transitions to "adv", starting from
    # a phase determined by replaying history. But E3 breaks it.
    #
    # I'll use: advance on capable action if (number of capable actions so far
    # in history, INCLUDING this one, is odd) OR ... no.
    #
    # Final decision: model advance as: capable action advances unless the
    # immediately preceding action was the SAME capable action AND that
    # preceding one advanced. Track per-action "last advanced" state.
    #   E2 A1,A1: 1st adv, 2nd prev same & adv -> no. ok.
    #   E4 A1,A1,A1: 1st adv, 2nd no, 3rd prev same but prev didn't adv -> adv.
    #     ok!
    #   E4 C30,C30: 1st adv, 2nd no. ok.
    #   E5 C30,C30: 1st adv, 2nd no. ok.
    #   E2 A3 after A1(no): diff action -> adv. ok.
    #   E2 A4 after A3(adv): diff action -> adv? observed no. FAIL.
    #   E1 C35 first: adv? observed no. Need start state.
    #   E3 C35 after A4(no,prev E4): diff -> adv ok. C30 after C15: diff->adv ok.
    # E2 A4 is the lone failure. Accept it.
    #
    # For first capable action ever (E1 C35): observed no. So if no prior
    # capable action, don't advance? But E2 A1 is first capable in E2 yet adv.
    # So it's not "first ever". E1 C35 was the very first action of the level.
    # Maybe: the very first action of the level never advances. E1 C35 = first
    # action -> no. E2 A1 is not first action of level (after E1's 4). ok.
    # E3 C35 not first. E4 A4 not first. E5 C30 not first.
    # So rule: advance if capable AND not (same as previous capable action that
    # advanced) AND not (this is the first action of the level).
    #
    # Good enough. Implement with history replay.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = list(probe.get("history", []) or [])

    def count_bands(fr):
        if not fr:
            return 0
        n = 0
        for k in range(10):
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

    def parse_click(a):
        try:
            p = a.split()
            return int(p[1]), int(p[2])
        except Exception:
            return None, None

    # Replay history to determine current band count and the "last capable
    # action that advanced" state.
    bands = count_bands(frame)
    last_adv_action = None  # the action string that most recently advanced
    prev_action = history[-1] if history else None
    level_started = (len(history) == 0)

    # We need to know, for each capable action, whether it advanced, to set
    # last_adv_action. Replay from scratch is hard without initial frame, so
    # approximate: we know current bands; we just need last_adv_action and
    # whether prev_action advanced. Use a heuristic: if prev_action was capable
    # and bands>0, assume it advanced unless it equals the action before it.
    # Simpler: track last_adv_action as the most recent capable action in
    # history that is NOT immediately preceded by an identical capable action.
    last_adv_action = None
    for i, a in enumerate(history):
        if is_adv_capable(a):
            if i == 0:
                # first action of level: does not advance
                continue
            prev = history[i - 1]
            if prev == a and last_adv_action == a:
                # repeated same action right after it advanced -> no advance
                continue
            last_adv_action = a

    steps = []
    for a in actions:
        changes = {}
        adv = False
        if is_adv_capable(a) and bands < 10:
            if level_started and not history and a == actions[0] and len(steps) == 0:
                # very first action of the level never advances
                adv = False
            elif a == last_adv_action and prev_action == a:
                adv = False
            else:
                adv = True
        if adv:
            r = 2 * bands
            for dr in (0, 1):
                for c in (62, 63):
                    changes["%d,%d" % (r + dr, c)] = '0'
            bands += 1
            last_adv_action = a
        # Target toggle on CLICK x in {30,35}: light a 3x3 block.
        if isinstance(a, str) and a.startswith("CLICK"):
            x, y = parse_click(a)
            if x in (30, 35):
                # block rows: round y to nearest block start (multiples of 5?)
                # observed blocks: y=50->49-51, y=55->54-56, y=60->59-61.
                # So block start = y-1 (for y=50->49, 55->54, 60->59).
                r0 = y - 1
                if x == 30:
                    cols = (29, 30, 31)
                else:
                    cols = (34, 35, 36)
                # toggle: e -> 0 -> 2 -> e ... (guess cycle e,0,2)
                # We don't track current colour reliably; predict 'e' first
                # time, else '0'. Use history count of clicks on this block.
                cnt = 0
                for h in history:
                    hx, hy = parse_click(h) if isinstance(h, str) and h.startswith("CLICK") else (None, None)
                    if hx == x and hy is not None and (hy - 1) == r0:
                        cnt += 1
                # also count within this probe so far
                for s in steps:
                    pass
                # cycle e,0,2
                cyc = ['e', '0', '2']
                col = cyc[cnt % 3]
                for rr in (r0, r0 + 1, r0 + 2):
                    for cc in cols:
                        changes["%d,%d" % (rr, cc)] = col
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
        prev_action = a
        level_started = False
    return {"steps": steps}
