def predict(probe):
    # Observations from the notebook:
    # The screen is 64x64. There is a "world" region and a HUD at the bottom row.
    # The bottom row (r63) is mostly 7s, with a 4 marker that moves left as
    # actions are taken: r63c63 -> r63c62 -> r63c61 [E1,E2,E3]. So the 4 in the
    # bottom row is a cursor/counter that moves LEFT by 1 per action (ACTION1-4).
    # ACTION5 does nothing [E1].
    #
    # The world region has blocks around columns 32-39. Actions shift blocks:
    #   - There appear to be two "columns" of content: cols 32-35 and cols 36-39.
    #   - ACTION4 moves content from cols 36-39 down/into cols 32-35 region
    #     (r48-51 c36-39 becomes 1, and c32-35 becomes 1) [E1 step1].
    #   - ACTION1 moves a block up by 4 rows: block at r40-43 c32-35 moves to
    #     r36-39 c32-35, leaving r40-43 as 1 [E2].
    #   - ACTION3 moves content from cols 32-35 into cols 36-39 (r44-47 c32-35
    #     becomes 1, c36-39 becomes 1) [E1 step3].
    #   - ACTION4 then ACTION3 etc. cycle blocks between the two column bands.
    #
    # This looks like a "15-puzzle"/sliding-block puzzle where blocks move in
    # 4-row steps within two vertical lanes (cols 32-35 and 36-39). The 4-marker
    # in the bottom row is a step counter that decrements per action.
    #
    # We don't know the win condition. Best guess (?): align the coloured blocks
    # into a target pattern; possibly the counter reaching 0, or blocks matching
    # a goal arrangement. Without evidence, predict the counter moving left by 1
    # per action (ACTION1-4), ACTION5 no-op, and no level completion.
    #
    # ? Goal: unknown; guessing NOT reached by these actions.

    actions = probe.get("actions", [])
    frame = probe.get("frame", None)
    steps = []
    for a in actions:
        changes = {}
        if a in ("ACTION1", "ACTION2", "ACTION3", "ACTION4"):
            # The 4-marker in the bottom row moves left by 1 each action.
            # Find its current column from the frame if available.
            if frame is not None:
                row63 = frame[63]
                col = row63.rfind("4")
                if col > 0:
                    changes["63,%d" % col] = "7"
                    changes["63,%d" % (col - 1)] = "4"
            # We can't reliably predict the block movements without full state
            # tracking; leave them out (best guess: only counter changes).
        # ACTION5: no change.
        steps.append({"changes": changes, "levels": 0, "state": "NOT_FINISHED"})
    return {"steps": steps}
