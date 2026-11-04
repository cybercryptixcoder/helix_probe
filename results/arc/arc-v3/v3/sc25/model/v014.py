def predict(probe):
    # Beliefs:
    # - Screen is 64x64 hex grid.
    # - There is a "player" 4-row structure around rows 19-22 that moves horizontally.
    #   ACTION1 shifts it left by 2 cols (and bar +2 rows) [E12,E13,E14]
    #   ACTION3 shifts it right by 2 cols (and bar +2 rows) [E12,E13,E14]
    #   ACTION2/ACTION4 toggle internal 9<->a colors [E2,E4,E11]
    # - Progress bar at cols 62-63 fills with 0 from top, ~2 rows per action [many]
    # - When bar reaches row 63, GAME_OVER [E15]
    # - CLICK on switch regions toggles e<->0 [E5,E7,E8,E18]
    # - CLICK elsewhere: no change [E1,E3,E6,E9,E17]
    # - RESET restores initial state [E16]
    #
    # GOAL (?): likely align player with a target switch position and toggle it,
    # or reach a specific column. Best guess: moving player far enough left/right
    # while bar not full. Marked uncertain.
    
    import copy
    
    actions = probe.get("actions", [])
    level = probe.get("level", 0)
    frame = probe.get("frame", None)
    history = probe.get("history", [])
    
    steps = []
    
    # Reconstruct current grid
    if frame is not None:
        grid = [list(row) for row in frame]
    else:
        grid = [['5']*64 for _ in range(64)]
    
    # Track bar fill level (rows filled from top with 0 at cols 62-63)
    # Count how many rows at top of cols 62-63 are '0'
    bar_fill = 0
    for r in range(64):
        if grid[r][62] == '0' and grid[r][63] == '0':
            bar_fill += 1
        else:
            break
    
    # Player position: find the 4-row block of 2s in rows 19-22
    # We'll track player left edge
    def find_player(g):
        # Look for rows 19-22 having 2s
        for r in range(19, 23):
            for c in range(64):
                if g[r][c] == '2':
                    # find leftmost 2 in this row
                    return c
        return 35  # default
    
    player_left = find_player(grid)
    
    # Player internal state: which colors where. We'll track a simplified model.
    # The player appears to be 4 rows x ~8 cols with pattern.
    
    state = "NOT_FINISHED"
    levels_done = 0
    
    for act in actions:
        changes = {}
        
        if state == "GAME_OVER":
            if act == "RESET":
                # restore initial - approximate
                state = "NOT_FINISHED"
                bar_fill = 0
                player_left = 35
                # We can't fully reconstruct; mark changes as unknown -> skip
                # For safety, produce no specific changes but reset state
                steps.append({"changes": {}, "levels": levels_done, "state": state})
                continue
            else:
                steps.append({"changes": {}, "levels": levels_done, "state": state})
                continue
        
        if act == "RESET":
            bar_fill = 0
            player_left = 35
            state = "NOT_FINISHED"
            steps.append({"changes": {}, "levels": levels_done, "state": state})
            continue
        
        if act in ("ACTION1", "ACTION3"):
            # Move player, fill bar
            if act == "ACTION1":
                player_left -= 2
            else:
                player_left += 2
            player_left = max(0, min(56, player_left))
            # Bar fills 2 rows
            for _ in range(2):
                if bar_fill < 64:
                    changes[f"{bar_fill},62"] = '0'
                    changes[f"{bar_fill},63"] = '0'
                    bar_fill += 1
            if bar_fill >= 64:
                state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue
        
        if act in ("ACTION2", "ACTION4"):
            # Toggle player internal colors; no bar fill in some cases
            # From E2: ACTION2 changed 8 cells (9<->a swap in part of player)
            # From E4: ACTION4 changed 12 cells including bar +2
            # Simplify: ACTION2 swaps a small region, ACTION4 swaps and fills bar
            if act == "ACTION4":
                for _ in range(2):
                    if bar_fill < 64:
                        changes[f"{bar_fill},62"] = '0'
                        changes[f"{bar_fill},63"] = '0'
                        bar_fill += 1
                if bar_fill >= 64:
                    state = "GAME_OVER"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue
        
        if act.startswith("CLICK"):
            parts = act.split()
            try:
                x = int(parts[1]); y = int(parts[2])
            except:
                steps.append({"changes": {}, "levels": levels_done, "state": state})
                continue
            # Switch regions: rows 49-51 and 54-56 and 59-61, cols 24-26/29-31/34-36
            toggled = False
            for (r0, c0) in [(49,29),(54,29),(54,24),(59,24),(49,34)]:
                if r0 <= y <= r0+2 and c0 <= x <= c0+2:
                    # toggle e<->0
                    cur = grid[y][x] if y < 64 and x < 64 else '5'
                    new = 'e' if cur == '0' else '0'
                    for rr in range(r0, r0+3):
                        for cc in range(c0, c0+3):
                            changes[f"{rr},{cc}"] = new
                    toggled = True
                    break
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue
        
        steps.append({"changes": {}, "levels": levels_done, "state": state})
    
    return {"steps": steps}
