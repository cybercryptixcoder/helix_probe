def predict(probe):
    # Model v2 — mechanism from E1-E3.
    #
    # Observations:
    #  - The screen has a "counter" in the top-right: rows 0..9 at cols 62-63 are
    #    background (5) initially; each CLICK on a "button" object advances it by
    #    turning the next pair of rows (r=2k, 2k+1) at cols 62-63 to 0 [E1,E2,E3].
    #    E1 CLICK 30 50 -> r0-1; E2 ACTION1 -> r2-3; E2 ACTION3 -> r4-5;
    #    E3 CLICK 35 60 -> r6-7; E3 CLICK 30 60 -> r8-9.  So each "advance"
    #    action fills the next 2-row band with 0.
    #  - There is a 3x3 block at rows 59-61, cols 29-31 or 34-36 that turns to e
    #    on some clicks [E1 r49-51 c29-31; E3 r59-61 c34-36; E3 r59-61 c29-31].
    #    These are "target" markers — the click x determines which column band.
    #  - ACTION2/ACTION3/ACTION4 rearrange a 4x4 region around rows 19-22,
    #    cols 35-42 (the "player"/puzzle area) [E1,E2].
    #
    # ? Goal guess: fill the top-right counter (all 10 bands -> 0) OR light up
    #   the correct target block.  Unproven.  We predict the counter advances
    #   on each click/action that visibly changed the counter in evidence.

    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", []) or []

    # Track counter state: number of 2-row bands already filled (0..5).
    # Replay history to know how many bands are already 0.
    def count_bands(fr):
        if not fr:
            return 0
        n = 0
        for k in range(5):
            r = 2 * k
            if r < len(fr) and len(fr[r]) > 63 and fr[r][62] == '0' and fr[r][63] == '0':
                n += 1
            else:
                break
        return n

    bands = count_bands(frame)

    # Which clicks advance the counter?  From evidence, clicks at x in {30,35}
    # (the "button" column) advance it.  Clicks elsewhere (15,16,63) do nothing.
    # ACTION1 also advances (E2).  ACTION3/ACTION4 do not advance the counter
    # (E2: ACTION3 changed r4-5 — wait, that DID advance).  Re-examine:
    #   E2 ACTION1 -> r2-3 (advance), ACTION1 -> nothing new on counter,
    #   ACTION3 -> r4-5 (advance), ACTION4 -> nothing on counter.
    # So ACTION1 and ACTION3 advance; ACTION2 and ACTION4 do not.
    # Clicks at x in {30,35} advance; other x do not.

    steps = []
    for a in actions:
        changes = {}
        if isinstance(a, str) and a.startswith("CLICK"):
            try:
                parts = a.split()
                x = int(parts[1]); y = int(parts[2])
            except Exception:
                x = y = -1
            if x in (30, 35) and bands < 5:
                r = 2 * bands
                for dr in (0, 1):
                    for c in (62, 63):
                        changes["%d,%d" % (r + dr, c)] = '0'
                bands += 1
                # target block at rows 59-61
                base = 34 if x == 35 else 29
                for rr in (59, 60, 61):
                    for cc in (base, base + 1, base + 2):
                        changes["%d,%d" % (rr, cc)] = 'e'
        elif a in ("ACTION1", "ACTION3"):
            if bands < 5:
                r = 2 * bands
                for dr in (0, 1):
                    for c in (62, 63):
                        changes["%d,%d" % (r + dr, c)] = '0'
                bands += 1
        # ACTION2, ACTION4, RESET: no counter change predicted here (unknown)
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
