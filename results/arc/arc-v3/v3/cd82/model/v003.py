def predict(probe):
    # Beliefs (evidence):
    # - Each CLICK on a listed object advances a hidden cursor one step LEFT along
    #   row 63, painting that cell 5. Cursor starts at col 64 (off-screen).
    #   Sequence of painted cells: c63 [E1], c62 [E1], c61 [E1], c60 [E2],
    #   c59 [E3], c58 [E3]. So the Nth ordinary click paints col 64-N. [E1,E2,E3]
    # - Some clicks change nothing visible: CLICK 8 5 first time [E2], CLICK 32 25
    #   [E3], CLICK 8 5 [E3]. These are clicks on objects already "used" (8 5 was
    #   used in E2) OR objects that don't advance the cursor. Notably CLICK 8 5
    #   advanced cursor in E2 (2nd click) but not in E3 — so it's not simply
    #   "already used". Pattern: the cursor only advances on SOME clicks.
    #   ? Hypothesis: cursor advances only when the clicked object is one of the
    #   "active" cursor objects; clicks on other objects do nothing. But 8 5
    #   advanced once (E2) and not later (E3) — so maybe each object can advance
    #   the cursor only once (consumed). 8 5 consumed in E2 -> inert in E3. [E2,E3]
    #   CLICK 32 25 inert [E3] - maybe already consumed? Not seen before, so ?
    #   Alternative: cursor advances on the FIRST click of each distinct object,
    #   subsequent clicks on same object inert. Check: 43 4 advanced in E1 (c63),
    #   then again in E1? no. 16 16 advanced (c62). 37 4 advanced (c61) AND
    #   toggled region. 8 5 first click inert [E2] — contradicts "first click
    #   advances". So 8 5 is special/inert object.
    # - CLICK 37 4 toggles a big region: r7 c35-39 and c41-45, r25-31 c26-37.
    #   Toggle between (0/3) and (3/0) for r7, and between 0 and f for the block.
    #   E1: ->0/3 and 0. E3: ->3/0 and f. So it alternates each click. [E1,E3]
    # - ACTION2 does nothing [E1].
    # ? Goal: unknown. Possibly fill row 63 fully, or toggle region to a target.
    #   We do NOT predict level completion yet (mark "?").
    #
    # Model: replay history to track (a) cursor column, (b) which objects have
    # been clicked (consumed), (c) region toggle parity.
    # Cursor advances on a click UNLESS the object is inert. We treat 8 5 as
    # inert-after-first? Actually 8 5 advanced on 2nd click in E2. Let's model:
    # cursor advances on a click if the object has NOT been clicked before in
    # history AND is not in a known-inert set. But 8 5 first click inert...
    # Simplify: cursor advances on every click EXCEPT clicks on objects in
    # INERT set {8 5, 32 25} when they are "fresh"? This is shaky.
    # Best fit to data: cursor advances on clicks to 43 4, 16 16, 37 4, 30 63,
    # 8 5(2nd in E2). Inert: 8 5(1st E2), 32 25(E3), 8 5(E3).
    # Rule guess: an object advances cursor only on its 2nd+ click? 43 4 E1 was
    # 1st click and advanced. No.
    # Rule guess: cursor advances on clicks to objects whose x,y are "cursor
    # objects"; 8 5 and 32 25 are not cursor objects. But 8 5 advanced in E2.
    # Contradiction. So 8 5 behavior depends on history: maybe it advances only
    # when cursor is at a specific column? E2 2nd click cursor was at 61->60.
    # Too speculative. Use: cursor advances on all clicks except a fixed inert
    # set {8 5, 32 25} — accept E2 mismatch on 8 5.
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
            if (x, y) == (37, 4):
                region_parity ^= 1
                cursor -= 1
            elif (x, y) in INERT:
                pass
            else:
                cursor -= 1
    for a in probe.get("actions", []):
        changes = {}
        if isinstance(a, str) and a.startswith("CLICK"):
            try:
                _, x, y = a.split()
                x, y = int(x), int(y)
            except Exception:
                x = y = -1
            if (x, y) == (37, 4):
                region_parity ^= 1
                if region_parity == 0:
                    # state A: r7 c35-39 -> 0, c41-45 -> 3; block -> 0
                    for c in range(35, 40):
                        changes["7,%d" % c] = 0
                    for c in range(41, 46):
                        changes["7,%d" % c] = 3
                    for r in range(25, 32):
                        for c in range(26, 38):
                            changes["%d,%d" % (r, c)] = 0
                else:
                    # state B: r7 c35-39 -> 3, c41-45 -> 0; block -> f
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
            elif (x, y) in INERT:
                pass
            else:
                cursor -= 1
                if 0 <= cursor < 64:
                    changes["63,%d" % cursor] = 5
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
