def predict(probe):
    # Model v6 — mechanism from E1-E8.
    #
    # Regions:
    #  - Top-right counter: rows 0..63 at cols 62-63. Each "advance" fills the
    #    next 2-row band (r=2k,2k+1) with 0, in order 0,2,4,...
    #    [E1 r0-1; E2 r2-3,r4-5; E3 r6-7,r8-9; E4 r10-11,r12-13,r14-15,r16-17;
    #     E5 r18-19; E6 r20-21,r22-23,r24-25,r26-27; E7 r28-29,r30-31;
    #     E8 r32-33]. Cap unknown; use 32.
    #  - Puzzle block rows 19-22, cols 35-42 (4x4 of 2x2 tiles). ACTION1/2/3/4
    #    permute the 2x2 tiles. Colours seen: 9,a,2.
    #  - Target blocks: CLICK x y lights a 3x3 block. x=30 -> cols 29-31,
    #    x=35 -> cols 34-36, x=25 -> cols 24-26. Row block start = y-1
    #    (y=50->49, 55->54, 60->59). Colour cycles e -> 0 -> 2 -> e ...
    #    per target block, by count of prior clicks on that exact block.
    #    [E4: e then 0; E5: e then 2; E6: 0 then e; E7: e; E8: 0,e,0]
    #
    # Advance rule (counter fills one band per "advance"):
    #   Capable actions: ACTION1, ACTION3, ACTION4, CLICK with x in {25,30,35}.
    #   ACTION2 is NOT capable. CLICK with x not in {25,30,35} is not capable.
    #
    #   Rule: a capable action advances UNLESS it is the same as the
    #   immediately preceding capable action AND that preceding one advanced.
    #   i.e. same-action-after-advance -> no advance (and flips flag).
    #   Same-action-after-no-advance -> advance. Different action -> advance.
    #   The very first action of the level never advances (E1 C35).
    #   [E8: C30,C30,C30 -> adv,no,adv matches this rule.]
    #
    #   Implement: replay history to get (bands, last_cap_action, last_cap_adv).

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
    last_cap = None
    last_cap_adv = False
    for i, a in enumerate(history):
        if not is_capable(a):
            continue
        if i == 0:
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

    for idx, a in enumerate(actions):
        changes = {}
        adv = False
        if is_capable(a) and bands < 32:
            if len(history) == 0 and idx == 0:
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
                else:
                    cols = (24, 25, 26)
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
