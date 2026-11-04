def predict(probe):
    # Beliefs:
    # - Grid layout fixed; only certain regions change [all E]
    # - Row 63 is a progress bar: a '4' marker moves LEFT by 1 per action; at c0 -> GAME_OVER [E32,E34,E35]
    #   RESET restores row63 to all 1 except marker at c63? Actually RESET restores level start [E33,E38,E40,E42,E44]
    # - 3/0 blocks at rows 48,49,59,60 in col-groups {15-19,22-26,29-33,36-40,43-47}.
    #   ACTION3/ACTION4 shift a "phase": exactly ONE group is 0 and the rest 3, and the 0-group
    #   advances by one group per ACTION3/ACTION4 press (wrapping). [E34,E35,E37,E41,E44,E45]
    #   E34: ACTION4 x6 -> 0-group goes g0,g1,g2,g3,g4,g0,g1 (each press advances one group).
    #   E45: ACTION4 -> g0=0, others 3 (only g0 changed from prior state where g0 was 3).
    #   E44: ACTION3 -> g0=3, g4=0 (advanced from g4? or from g0->g4 wrap). Model: advance index +1 mod 5.
    # - Tile region rows 51-58 (5x5 interiors at tile columns). ACTION1 toggles a fixed sparse
    #   subset of the active tile's 5x5 interior; ACTION2 toggles the COMPLEMENT subset (5<->7 swap
    #   on those cells). Active tile chosen by cursor column. [E46,E39,E42,E43,E44]
    #   E46: ACTION1 then ACTION2 on same tile -> second undoes first exactly (complement). 
    # - RESET restores level start (blocks, tiles, row63). [E33,E38,E40,E42,E44]
    # - GOAL (?): unknown; possibly align blocks or tiles. Unproven.
    import copy
    frame = probe.get("frame")
    history = probe.get("history", [])
    actions = probe.get("actions", [])
    level = probe.get("level", 0)

    grid = [list(row) for row in frame] if frame else [['2']*64 for _ in range(64)]

    # marker column
    marker_col = 63
    if frame:
        r63 = frame[63]
        for c in range(64):
            if r63[c] == '4':
                marker_col = c
                break
        else:
            marker_col = 63

    # 3/0 block groups
    groups = [(15,19),(22,26),(29,33),(36,40),(43,47)]
    # find current zero-group index (group whose row48 is '0'); default 0
    zero_idx = 0
    if frame:
        for i,g in enumerate(groups):
            if frame[48][g[0]] == '0':
                zero_idx = i
                break

    # tile interior: 5x5 interiors. Tiles at columns: left tile ~ c15-19, right ~ c43-47, etc.
    # We model the active tile's interior toggle as a fixed sparse subset. Since we don't know
    # exact subset per tile, approximate: ACTION1 toggles a fixed set of cells in the active tile,
    # ACTION2 toggles the complement. We use the observed E46 subset for the leftmost tile.
    # Active tile column base from cursor: tiles at 15,22,29,36,43 (5 tiles across region A).
    tile_bases = [15,22,29,36,43]
    # choose tile by marker_col mapping: cursor col -> tile index
    # approximate: tile index = clamp((marker_col-15)//7,0,4) but marker is on row63 far right;
    # Evidence suggests active tile relates to cursor. Use nearest tile base.
    ti = 0
    if frame:
        best = 1e9
        for i,b in enumerate(tile_bases):
            d = abs(marker_col - b)
            if d < best:
                best = d; ti = i
    base = tile_bases[ti]

    # ACTION1 subset (relative offsets within 5x5 interior rows 52-56, cols base..base+4)
    # From E46 ACTION1 on tile0: changed cells (row,col): 
    # r52 c15,16,18,19 ; r53 c15,17,18 ; r54 c15,16,17 ; r55 c15 ; r56 c17,19
    a1_offsets = set()
    for (r,c) in [(52,15),(52,16),(52,18),(52,19),(53,15),(53,17),(53,18),
                  (54,15),(54,16),(54,17),(55,15),(56,17),(56,19)]:
        a1_offsets.add((r-52, c-15))
    # complement within 5x5 interior
    all_off = set((r,c) for r in range(5) for c in range(5))
    a2_offsets = all_off - a1_offsets

    steps = []
    for act in actions:
        changes = {}
        state = "NOT_FINISHED"
        levels = 0

        if act == "RESET":
            # restore level start: row63 all 1 with marker at 63? Observed RESET sets row63 to 1s
            # and marker somewhere. Approximate: row63 all '1', marker at 63.
            for c in range(64):
                if frame and frame[63][c] != '1':
                    changes[f"63,{c}"] = '1'
            marker_col = 63
            zero_idx = 0
        else:
            # advance progress marker left by 1
            if marker_col > 0:
                new_col = marker_col - 1
                changes[f"63,{marker_col}"] = '1'
                changes[f"63,{new_col}"] = '4'
                marker_col = new_col
            else:
                state = "GAME_OVER"

            if act in ("ACTION3", "ACTION4"):
                # advance zero-group by one (wrap)
                old = zero_idx
                new = (zero_idx + 1) % 5
                # set old group to 3, new group to 0
                for r in (48,49,59,60):
                    for c in range(groups[old][0], groups[old][1]+1):
                        if frame and frame[r][c] in ('3','0'):
                            changes[f"{r},{c}"] = '3'
                    for c in range(groups[new][0], groups[new][1]+1):
                        if frame and frame[r][c] in ('3','0'):
                            changes[f"{r},{c}"] = '0'
                zero_idx = new
            elif act == "ACTION1":
                for (dr,dc) in a1_offsets:
                    r = 52+dr; c = base+dc
                    if frame and frame[r][c] in ('5','7'):
                        changes[f"{r},{c}"] = '7' if frame[r][c]=='5' else '5'
            elif act == "ACTION2":
                for (dr,dc) in a2_offsets:
                    r = 52+dr; c = base+dc
                    if frame and frame[r][c] in ('5','7'):
                        changes[f"{r},{c}"] = '7' if frame[r][c]=='5' else '5'

        for k,v in changes.items():
            r,c = map(int, k.split(','))
            grid[r][c] = v
        frame = [''.join(row) for row in grid]

        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
