def predict(probe):
    # Beliefs:
    # - Grid is a fixed layout; only certain regions change [all E]
    # - Row 63 is a progress bar: color 4 marker moves left 1 per action; at c0 -> GAME_OVER [E32]
    # - Small 3/0 blocks at rows 48,49,59,60, col-groups {15-19,22-26,29-33,36-40,43-47}
    #   toggle between 3 and 0. ACTION3 and ACTION4 flip them in alternating fashion [E1,E2,E3,E4,E5]
    # - Tile region rows 51-58 cycles glyph patterns via ACTION1; ACTION2 swaps 5<->7 [E2,E17,E18]
    # - RESET restores level start [E33]
    # - GOAL (?): likely make 3/0 blocks uniform or match target; unproven.
    import copy
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])
    level = probe.get("level", 0)

    # We cannot fully simulate glyph cycles without exact tables; we model the
    # well-evidenced parts (progress bar, 3/0 toggles) and leave glyphs to
    # approximate cycling. Prediction focuses on structure.

    grid = [list(row) for row in frame] if frame else [['2']*64 for _ in range(64)]

    # Determine current progress marker column from row 63
    # Row 63: '1'*k then '4' at col k then '1'... Actually marker at some col.
    marker_col = 63
    if frame:
        r63 = frame[63]
        for c in range(64):
            if r63[c] == '4':
                marker_col = c
                break
        else:
            marker_col = 63

    # Track 3/0 block state: which groups are 3 vs 0.
    # Groups: g0=15-19, g1=22-26, g2=29-33, g3=36-40, g4=43-47
    groups = [(15,19),(22,26),(29,33),(36,40),(43,47)]
    # Read current: block at row48 group is 3 or 0
    def read_blocks(g):
        if not frame: return None
        return frame[48][g[0]]

    steps = []
    for act in actions:
        changes = {}
        state = "NOT_FINISHED"
        levels = 0

        if act == "RESET":
            # restore initial: approximate by resetting row63 to all 1, blocks to 3/0 default
            # We can't know exact initial; emit full-ish reset of row63
            for c in range(64):
                changes[f"63,{c}"] = '1'
            marker_col = 63
            state = "NOT_FINISHED"
        else:
            # advance progress marker left by 1
            if marker_col > 0:
                new_col = marker_col - 1
                changes[f"63,{marker_col}"] = '1'
                changes[f"63,{new_col}"] = '4'
                marker_col = new_col
            else:
                # already at 0 -> next action triggers game over
                state = "GAME_OVER"

            if act in ("ACTION3", "ACTION4"):
                # toggle 3/0 blocks: set first two groups swapped
                # Evidence: ACTION4 sets g0=3,g1=0; ACTION3 sets g0=0,g1=3 (relative flips)
                # Model as: toggle all block groups between 3 and 0
                for g in groups:
                    cur = read_blocks(g)
                    if cur is not None:
                        newv = '0' if cur == '3' else '3'
                        for r in (48,49,59,60):
                            for c in range(g[0], g[1]+1):
                                if frame and frame[r][c] in ('3','0'):
                                    changes[f"{r},{c}"] = newv
            elif act == "ACTION1":
                # cycle tile glyphs; approximate: leave as-is (unknown table)
                pass
            elif act == "ACTION2":
                # swap 5<->7 in tile region rows 51-58
                for r in range(51,59):
                    for c in range(64):
                        if frame and frame[r][c] in ('5','7'):
                            changes[f"{r},{c}"] = '7' if frame[r][c]=='5' else '5'

        # apply changes to grid for next step
        for k,v in changes.items():
            r,c = map(int, k.split(','))
            grid[r][c] = v
        frame = [''.join(row) for row in grid]

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
