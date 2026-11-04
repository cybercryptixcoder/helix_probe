def predict(probe):
    # Beliefs (evidence):
    # - Every non-inert CLICK advances a hidden cursor one step LEFT along row 63,
    #   painting that cell 5. Cursor starts at col 64 (off-screen).
    #   Painted cells in order: c63 [E1], c62 [E1], c61 [E1], c60 [E2],
    #   c59 [E3], c58 [E3], c57 [E4], c56 [E4], c55 [E4], c54 [E5],
    #   c53 [E6], c52 [E6]. [E1..E6]
    # - CLICK 8 5 is INERT (never advances, never paints) [E2,E3,E4].
    # - CLICK 32 25 is INERT [E3].
    # - CLICK 37 4 / 41 4 / 43 4 / 43 7 / 16 16 / 30 63 / 32 39 / 40 4 all
    #   advance the cursor (non-inert). [E1..E6]
    # - CLICK 37 4 and CLICK 41 4 toggle a big region AND advance cursor:
    #   r7 c35-39 & c41-45 swap (0/3)<->(3/0); block r25-31 c26-37 swaps 0<->f.
    #   State alternates each such click. [E1,E3,E5,E6]
    # - ACTION2 does nothing [E1].
    # - ACTION5 fills block r34-38 c27-36 with f [E7].
    # - ACTION4 draws a big sprite/pattern (triangle+fan) [E7].
    # - CLICK 16 16 after ACTION4 did nothing here [E7] (may be inert or
    #   already-painted; treat as inert for now). ?
    # ? Goal: unknown. Possibly fill row 63 fully. We do NOT predict completion.
    INERT = {(8, 5), (32, 25), (16, 16)}
    TOGGLE = {(37, 4), (41, 4)}
    steps = []
    hist = probe.get("history", []) or []
    cursor = 64
    region_parity = 0  # 0 = state A (r7 0/3, block 0), 1 = state B (r7 3/0, block f)
    for h in hist:
        if isinstance(h, str) and h.startswith("CLICK"):
            try:
                _, x, y = h.split()
                x, y = int(x), int(y)
            except Exception:
                continue
            if (x, y) in INERT:
                continue
            if (x, y) in TOGGLE:
                region_parity ^= 1
            cursor -= 1
    for a in probe.get("actions", []):
        changes = {}
        if isinstance(a, str) and a.startswith("CLICK"):
            try:
                _, x, y = a.split()
                x, y = int(x), int(y)
            except Exception:
                x = y = -1
            if (x, y) in INERT:
                pass
            else:
                if (x, y) in TOGGLE:
                    region_parity ^= 1
                    if region_parity == 0:
                        for c in range(35, 40):
                            changes["7,%d" % c] = 0
                        for c in range(41, 46):
                            changes["7,%d" % c] = 3
                        for r in range(25, 32):
                            for c in range(26, 38):
                                changes["%d,%d" % (r, c)] = 0
                    else:
                        for c in range(35, 40):
                            changes["7,%d" % c] = 3
                        for c in range(41, 46):
                            changes["7,%d" % c] = 0
                        for r in range(25, 32):
                            for c in range(26, 38):
                                changes["%d,%d" % (r, c)] = 0xf
                cursor -= 1
                if 0 <= cursor < 64:
                    changes["63,%d" % cursor] = 5
        elif a == "ACTION5":
            for r in range(34, 39):
                for c in range(27, 37):
                    changes["%d,%d" % (r, c)] = 0xf
        elif a == "ACTION4":
            # Big sprite: approximate from E7 observation.
            sprite = {
                (21, 39): 2,
                (22, 38): 2, (22, 39): 2, (22, 40): 2,
                (23, 37): 2, (23, 38): 2, (23, 39): 0xf, (23, 40): 2, (23, 41): 2,
            }
            for r in range(24, 33):
                for c in range(25, 50):
                    sprite[(r, c)] = 5
            for r in range(24, 35):
                for c in range(38, 50):
                    sprite[(r, c)] = 0xf
            for (r, c), v in sprite.items():
                changes["%d,%d" % (r, c)] = v
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
