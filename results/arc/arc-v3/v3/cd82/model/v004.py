def predict(probe):
    # Beliefs (evidence):
    # - Each CLICK on a listed object advances a hidden cursor one step LEFT along
    #   row 63, painting that cell 5. Cursor starts at col 64 (off-screen).
    #   Painted cells in order: c63 [E1], c62 [E1], c61 [E1], c60 [E2],
    #   c59 [E3], c58 [E3], c57 [E4], c56 [E4], c55 [E4]. [E1,E2,E3,E4]
    # - Some clicks change nothing: CLICK 8 5 [E2 first], CLICK 32 25 [E3],
    #   CLICK 8 5 [E3], CLICK 8 5 [E4]. These objects are INERT: they never
    #   advance the cursor and never paint. 8 5 and 32 25 are inert. [E2,E3,E4]
    # - CLICK 37 4 toggles a big region AND advances cursor: r7 c35-39 and
    #   c41-45 swap (0/3)<->(3/0); block r25-31 c26-37 swaps 0<->f. [E1,E3]
    #   E1: ->0/3 and 0. E3: ->3/0 and f. Alternates each click.
    # - ACTION2 does nothing [E1].
    # ? Goal: unknown. Possibly fill row 63 fully. We do NOT predict completion.
    INERT = {(8, 5), (32, 25)}
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
            if (x, y) == (37, 4):
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
                if (x, y) == (37, 4):
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
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
