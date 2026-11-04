def predict(probe):
    # Model v7 — mechanism from E1-E9.
    #
    # Regions:
    #  - Top-right counter: rows 0..63 at cols 62-63. Each "advance" fills the
    #    next 2-row band (r=2k,2k+1) with 0, in order 0,2,4,...
    #  - Puzzle block rows 19-22, cols 35-42 (4x4 of 2x2 tiles). ACTION1/2/3/4
    #    permute the 2x2 tiles. Colours seen: 9,a,2.
    #  - Target blocks: CLICK x y lights a 3x3 block. x=30 -> cols 29-31,
    #    x=35 -> cols 34-36, x=25 -> cols 24-26. Row block start = y-1.
    #    Colour per block depends on the count of prior clicks on that exact
    #    block (across the whole level): odd count -> 'e', even count -> '0',
    #    EXCEPT block (30,55) whose even count -> '2'. [E1,E4,E6,E8,E9 for
    #    (30,50); E5,E7 for (30,55); E6,E9 for (25,55); E7 for (25,60);
    #    E1,E6 for (35,50)]
    #
    # Advance rule (counter fills one band per "advance"):
    #   Capable actions: ACTION1, ACTION3, ACTION4, CLICK with x in {25,30,35}.
    #   ACTION2 is NOT capable. CLICK with x not in {25,30,35} is not capable.
    #   Rule: a capable action advances UNLESS it is the same as the
    #   immediately preceding capable action AND that preceding one advanced.
    #   The very first action of the level is a complete no-op (no advance,
    #   no colour) [E1 step1: CLICK 35 50 -> 0 changes].

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
        is_first_of_level = (len(history) == 0 and idx == 0)
        adv = False
        if is_capable(a) and bands < 32 and not is_first_of_level:
            if a == last_cap and last_cap_adv:
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

        # Target block on CLICK x in {25,30,35}, unless first action of level.
        if isinstance(a, str) and a.startswith("CLICK") and not is_first_of_level:
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
                if cnt % 2 == 0:
                    col = 'e'
                else:
                    col = '2' if (x == 30 and y == 55) else '0'
                for rr in (r0, r0 + 1, r0 + 2):
                    for cc in cols:
                        changes["%d,%d" % (rr, cc)] = col

        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})

    return {"steps": steps}
