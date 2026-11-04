def predict(probe):
    # Model v5 — mechanism from E1-E7.
    #
    # Regions:
    #  - Top-right counter: rows 0..31 at cols 62-63. Each "advance" fills the
    #    next 2-row band (r=2k,2k+1) with 0. Bands fill in order 0,2,4,...
    #    [E1 r0-1; E2 r2-3,r4-5; E3 r6-7,r8-9; E4 r10-11,r12-13,r14-15,r16-17;
    #     E5 r18-19; E6 r20-21,r22-23,r24-25,r26-27; E7 r28-29,r30-31].
    #    So at least 16 bands (rows 0..31). Cap unknown; use 32.
    #  - Puzzle block rows 19-22, cols 35-42 (4x4 of 2x2 tiles). ACTION1/2/3/4
    #    permute the 2x2 tiles. Colours seen: 9,a,2.
    #  - Target blocks: CLICK x y lights a 3x3 block. x=30 -> cols 29-31,
    #    x=35 -> cols 34-36, x=25 -> cols 24-26. Row block start = y-1
    #    (y=50->49, 55->54, 60->59). Colour cycles e -> 0 -> 2 -> e ...
    #    per target block (E4: e then 0; E5: e then 2; E6: 0 then e; E7: e).
    #    Actually per-block click count cycles e,0,2.
    #
    # Advance rule (counter fills one band per "advance"):
    #   Capable actions: ACTION1, ACTION3, ACTION4, CLICK with x in {25,30,35}.
    #   ACTION2 is NOT capable (E2: A2 no advance; E4: A2 no advance).
    #   CLICK with x not in {25,30,35} is not capable (E1 C16, E3 C15, E6 C16).
    #
    #   Sequence of capable actions and adv/no across all evidence:
    #   E1: C35(no), C30(adv)
    #   E2: A1(adv), A1(no), A3(adv), A4(no)
    #   E3: C35(adv), C30(adv)
    #   E4: A4(adv), C30(adv), C30(no), A1(adv), A1(no), A1(adv)
    #   E5: C30(adv), C30(no)
    #   E6: C25(adv), A3(adv), C30(adv), C30(no), C35(adv)
    #   E7: C30(adv), A4(adv), C25(adv)
    #
    #   Key: E1 C35 first action of level -> no. E6 C25 not first -> adv.
    #   E7 C30 not first -> adv.
    #   Repeats: same action twice -> adv then no (E4 C30,C30; E5 C30,C30;
    #   E6 C30,C30; E2 A1,A1). Three times -> adv,no,adv (E4 A1,A1,A1).
    #   Different action after adv -> adv (E3 C35,C30; E4 A4,C30; E6 C25,A3;
    #   E7 C30,A4,C25). Different action after no -> adv (E2 A3 after A1no;
    #   E6 C35 after C30no).
    #
    #   So: a capable action advances UNLESS it is the same as the immediately
    #   preceding capable action AND that preceding one advanced. i.e. track
    #   last capable action and whether it advanced; if same action and it
    #   advanced, this one does not advance (and flips the flag). If same
    #   action and it did NOT advance, this one advances.
    #   Also: the very first action of the level never advances (E1 C35).
    #   Check E2 A4 after A3(adv): different -> should adv, but observed no.
    #   This is the one exception. E2 A4 is the only "different after adv -> no".
    #   Accept as noise / unknown.
    #
    #   Implement: replay history to get (bands, last_cap_action, last_cap_adv).
    #   Since we can't replay from scratch without initial frame, use current
    #   bands from frame, and infer last_cap_action/adv from history tail.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = list(probe.get("history", []) or [])

    def count_bands(fr):
        if not fr:
            return 0
        n = 0
        for k in range(32):
            r = 2 * k
            if r < len(fr) and len(fr[r]) > 63 and fr[r][62] == '0' and fr[r][63] == '0':
                n += 1
            else:
                break
        return n

    def parse_click(a):
        try:
            p = a.split()
            return int(p[1]), int(p[2])
        except Exception:
            return None, None

    def is_capable(a):
        if not isinstance(a, str):
            return False
        if a in ("ACTION1", "ACTION3", "ACTION4"):
            return True
        if a.startswith("CLICK"):
            x, y = parse_click(a)
            return x in (25, 30, 35)
        return False

    # Replay history to determine last capable action and whether it advanced.
    # We approximate "advanced" by the same-action rule.
    last_cap = None
    last_cap_adv = False
    for i, a in enumerate(history):
        if not is_capable(a):
            continue
        if i == 0:
            # first action of level: never advances
            last_cap = a
            last_cap_adv = False
            continue
        if a == last_cap and last_cap_adv:
            last_cap_adv = False
        else:
            last_cap_adv = True
        last_cap = a

    bands = count_bands(frame)
    steps = []
    first_action = (len(history) == 0)

    for idx, a in enumerate(actions):
        changes = {}
        adv = False
        if is_capable(a) and bands < 32:
            if first_action and idx == 0 and len(history) == 0:
                adv = False
            elif a == last_cap and last_cap_adv:
                adv = False
            else:
                adv = True
        if adv:
            r = 2 * bands
            for dr in (0, 1):
                for c in (62, 63):
                    changes["%d,%d" % (r + dr, c)] = '0'
            bands += 1
            last_cap_adv = True
        else:
            if is_capable(a):
                last_cap_adv = False
        if is_capable(a):
            last_cap = a

        # Target block on CLICK x in {25,30,35}
        if isinstance(a, str) and a.startswith("CLICK"):
            x, y = parse_click(a)
            if x in (25, 30, 35):
                r0 = y - 1
                if x == 30:
                    cols = (29, 30, 31)
                elif x == 35:
                    cols = (34, 35, 36)
                else:  # x == 25
                    cols = (24, 25, 26)
                # count prior clicks on this exact block (history + this probe)
                cnt = 0
                for h in history:
                    if isinstance(h, str) and h.startswith("CLICK"):
                        hx, hy = parse_click(h)
                        if hx == x and hy is not None and (hy - 1) == r0:
                            cnt += 1
                for j in range(idx):
                    pa = actions[j]
                    if isinstance(pa, str) and pa.startswith("CLICK"):
                        px, py = parse_click(pa)
                        if px == x and py is not None and (py - 1) == r0:
                            cnt += 1
                cyc = ['e', '0', '2']
                col = cyc[cnt % 3]
                for rr in (r0, r0 + 1, r0 + 2):
                    for cc in cols:
                        changes["%d,%d" % (rr, cc)] = col

        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})

    return {"steps": steps}
