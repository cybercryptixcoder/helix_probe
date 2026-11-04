def predict(probe):
    # Beliefs (evidence):
    # - Clicks on listed objects usually change nothing visible [E2 first click].
    # - A click can change a single cell at row 63 (bottom row), moving right-to-left:
    #   r63 c63 [E1], r63 c62 [E1], r63 c61 [E1], r63 c60 [E2]. So each click on a
    #   "fresh" object advances a hidden cursor one step left along row 63. [E1,E2]
    # - CLICK 37 4 also triggered a big region change (r7, r25-31) [E1] — likely a
    #   special object/switch; ? unclear, treat as region toggle.
    # - ACTION2 changed nothing [E1].
    # ? Goal: unknown; likely clicking the right object(s). We do NOT predict level
    #   completion yet (mark "?").
    #
    # Model: maintain a hidden cursor column on row 63 starting at 64 (off-screen).
    # Each click on a listed object (except the special 37,4) moves cursor left by 1
    # and paints that cell 5. Clicking 37,4 toggles the big region.
    steps = []
    # We can't see history reliably; use probe history if present to seed cursor.
    hist = probe.get("history", []) or []
    # Count clicks on ordinary objects since level start to estimate cursor position.
    # Cursor starts at col 64; each ordinary click decrements.
    ordinary = 0
    for h in hist:
        if isinstance(h, str) and h.startswith("CLICK"):
            try:
                _, x, y = h.split()
                x, y = int(x), int(y)
            except Exception:
                continue
            if (x, y) == (37, 4):
                continue
            ordinary += 1
    # Also account for clicks in this probe as we go.
    cursor = 64 - ordinary  # next click paints cursor-1
    for a in probe.get("actions", []):
        changes = {}
        if isinstance(a, str) and a.startswith("CLICK"):
            try:
                _, x, y = a.split()
                x, y = int(x), int(y)
            except Exception:
                x = y = -1
            if (x, y) == (37, 4):
                # ? toggle big region: guess it flips r7 c35-45 and r25-31 c26-37
                # We don't know current state; emit a plausible toggle set.
                for c in range(35, 46):
                    changes["7,%d" % c] = 0 if c < 41 else 3
                for r in range(25, 32):
                    for c in range(26, 38):
                        changes["%d,%d" % (r, c)] = 0
            else:
                cursor -= 1
                if 0 <= cursor < 64:
                    changes["63,%d" % cursor] = 5
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
