def predict(probe):
    # Beliefs:
    # - Grid layout fixed; only certain regions change [all E]
    # - Row 63 is a progress bar: a '4' marker moves LEFT by 1 per action; at c0 -> GAME_OVER [E32,E34,E35]
    #   RESET restores row63 to all 1 with marker at c63 [E33,E38,E40,E42,E44]
    # - 3/0 blocks at rows 48,49,59,60 in col-groups {15-19,22-26,29-33,36-40,43-47}.
    #   Exactly ONE group is 0 and the rest 3; ACTION3/ACTION4 advances the 0-group by one
    #   (wrapping) [E34,E35,E37,E41,E44,E45,E47].
    #   E47: ACTION4 -> g0=3, g1=0 (advanced from g0). E45: ACTION4 -> g0=0 (from g4 wrap).
    # - Tile region rows 51-58 (5x5 interiors at tile columns 15,22,29,36,43).
    #   ACTION1 toggles a fixed sparse subset of the active tile's 5x5 interior;
    #   ACTION2 toggles the COMPLEMENT subset (5<->7 swap). [E46,E39,E42,E43,E44,E47]
    #   Active tile is chosen by cursor column (marker_col). [E4,E8,E10,E12,E14]
    #   E47: cursor at c60 -> active tile g4 (base 43). E43: cursor c62 -> tile g4? no, observed c15.
    #   Actually E43 cursor c62 -> tile g0 (c15). E44 cursor c63 -> tile g4 (c43).
    #   E46 cursor c61 -> tile g0 (c15). E47 cursor c60 -> tile g0 (c15).
    #   So mapping is NOT simple nearest. Observed: c60->g0, c61->g0, c62->g0, c63->g4.
    #   Model: tile index = (marker_col // 7) % 5? c60//7=8%5=3 no. 
    #   Try: ti = (63 - marker_col) // 7? c60: 3//7=0 -> g0 ok. c63: 0//7=0 -> g0 but obs g4.
    #   Hmm. Use: ti = (63 - marker_col) // 7, but c63 special? Actually E44 c63->g4.
    #   Let's use ti = ((63 - marker_col) // 7) % 5 but c63 -> 0. Conflict.
    #   Alternative: ti = (marker_col - 15) // 7 clamped? c60: 45//7=6 -> clamp 4 = g4 no.
    #   Observed data: c60->g0, c61->g0, c62->g0, c63->g4. Only c63 differs.
    #   Maybe cursor wraps: after RESET marker at 63 = tile g4? E44 RESET then ACTION3 then ACTION2
    #   at cursor 63 -> tile g4 (c43). E46 starts cursor 61 -> g0. E43 cursor 62 -> g0.
    #   So c63->g4, c60/61/62->g0. Use: ti = 4 if marker_col==63 else 0? crude.
    #   Better: ti = (63 - marker_col) // 7 gives c63:0, c62:0, c61:0, c60:0. Then c63 wrong.
    #   Use ti = ((63 - marker_col) // 7) and if marker_col==63: ti=4. Mark "?".
    # - RESET restores level start (blocks, tiles, row63). [E33,E38,E40,E42,E44]
    # - GOAL (?): unknown; possibly align blocks or tiles. Unproven.
    import copy
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])
    level = probe.get("level", 0)

    grid = [list(row) for row in frame] if frame else [['2']*64 for _ in range(64)]

    marker_col = 63
    if frame:
        r63 = frame[63]
        for c in range(64):
            if r63[c] == '4':
                marker_col = c
                break
        else:
            marker_col = 63

    groups = [(15,19),(22,26),(29,33),(36,40),(43,47)]
    zero_idx = 0
    if frame:
        for i,g in enumerate(groups):
            if frame[48][g[0]] == '0':
                zero_idx = i
                break

    tile_bases = [15,22,29,36,43]

    def active_tile(mc):
        # observed: c60,61,62 -> g0; c63 -> g4
        if mc == 63:
            return 4
        return 0

    # ACTION1 subset (relative offsets within 5x5 interior rows 52-56, cols base..base+4)
    a1_offsets = set()
    for (r,c) in [(52,15),(52,16),(52,18),(52,19),(53,15),(53,17),(53,18),
                  (54,15),(54,16),(54,17),(55,15),(56,17),(56,19)]:
        a1_offsets.add((r-52, c-15))
    all_off = set((r,c) for r in range(5) for c in range(5))
    a2_offsets = all_off - a1_offsets

    steps = []
    for act in actions:
        changes = {}
        state = "NOT_FINISHED"
        levels = 0

        if act == "RESET":
            for c in range(64):
                if frame and frame[63][c] != '1':
                    changes[f"63,{c}"] = '1'
            marker_col = 63
            zero_idx = 0
        else:
            if marker_col > 0:
                new_col = marker_col - 1
                changes[f"63,{marker_col}"] = '1'
                changes[f"63,{new_col}"] = '4'
                marker_col = new_col
            else:
                state = "GAME_OVER"

            if act in ("ACTION3", "ACTION4"):
                old = zero_idx
                new = (zero_idx + 1) % 5
                for r in (48,49,59,60):
                    for c in range(groups[old][0], groups[old][1]+1):
                        if frame and frame[r][c] in ('3','0'):
                            changes[f"{r},{c}"] = '3'
                    for c in range(groups[new][0], groups[new][1]+1):
                        if frame and frame[r][c] in ('3','0'):
                            changes[f"{r},{c}"] = '0'
                zero_idx = new
            elif act in ("ACTION1", "ACTION2"):
                ti = active_tile(marker_col)
                base = tile_bases[ti]
                offs = a1_offsets if act == "ACTION1" else a2_offsets
                for (dr,dc) in offs:
                    r = 52+dr; c = base+dc
                    if frame and frame[r][c] in ('5','7'):
                        changes[f"{r},{c}"] = '7' if frame[r][c]=='5' else '5'

        for k,v in changes.items():
            r,c = map(int, k.split(','))
            grid[r][c] = v
        frame = [''.join(row) for row in grid]

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
