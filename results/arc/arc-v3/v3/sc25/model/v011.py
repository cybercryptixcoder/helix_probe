def predict(probe):
    # Model of the black box.
    #
    # Beliefs (from evidence):
    # - Grid 64x64 of hex digits; background '5'.
    # - CLICK on a "block" object toggles its colour; CLICK on background does nothing.
    # - ACTION1..ACTION4 are global actions that advance a "tick".
    # - The right-edge bar (cols 62-63) fills 2 rows per tick, top-down, from row 0.
    #   Each ACTION or "tick" CLICK advances it by exactly 2 rows [E3,E4,E5,E6,E7,E8,E9,E10,E11,E12,E13,E14].
    # - The bar is a COUNTDOWN/timer, not a win condition: it reached row 63 in E14
    #   (after 57 actions) with levels still 0, and the very next action (E15) gave
    #   GAME_OVER with 0 changes. So the bar running out = GAME_OVER [E14, E15].
    # - So the goal is NOT "fill the bar". The bar is a time limit.
    # - The 4x4 dial at rows 19-22 (cols ~23-42) changes on ACTION1/ACTION3/ACTION4:
    #   ACTION1 and ACTION3 alternate a 2x2 '9'/'a' pair and shift the pattern left by
    #   ~2-4 columns each time; ACTION4 sets a wide '2/a/9' pattern [E2,E4,E6,E7,E10,E11,E12,E13,E14].
    # - Blocks: 3x3 'e' blocks at (49,29),(49,34),(54,29),(54,24),(59,34),(59,24).
    #   Clicking cycles e->0->2->e (or e->0->e); each click also advances the bar [E1,E3,E4,E5,E6,E7,E8,E9,E10].
    # - GAME_OVER: only RESET works. After GAME_OVER, actions do nothing (E15: 0 changes).
    #
    # GOAL (best guess, marked "?"): The dial must be aligned to a target configuration
    # (probably the 2x2 '9' pair centered, or a specific pattern) BEFORE the bar runs out.
    # The bar is a timer; completing the dial alignment completes the level.
    # We do NOT know the exact target. We guess: level completes when the dial shows
    # a specific pattern. Since we can't verify, we mark "?" and do not predict WIN
    # from bar-fill alone (that was the v9 error).

    import re

    actions = probe.get("actions", [])
    level = probe.get("level", 0)
    frame = probe.get("frame", None)
    history = probe.get("history", [])

    if frame is not None:
        grid = [list(row) for row in frame]
    else:
        grid = [['5'] * 64 for _ in range(64)]

    def set_cell(r, c, val):
        if 0 <= r < 64 and 0 <= c < 64:
            grid[r][c] = val

    def get_cell(r, c):
        if 0 <= r < 64 and 0 <= c < 64:
            return grid[r][c]
        return '5'

    # --- Bar / tick model ---
    # Each ACTION or tick-CLICK advances bar by 2 rows. Bar fills from row 0.
    # When bar reaches bottom (row 62-63 filled), next tick => GAME_OVER.
    # We track "ticks" = number of bar-advancing actions since level start.
    # From history we can't know initial tick count, but frame shows current bar.
    # We infer current filled rows from frame: count leading rows where c62=='0'.
    filled_rows = 0
    for r in range(64):
        if get_cell(r, 62) == '0':
            filled_rows += 1
        else:
            break
    # ticks so far = filled_rows / 2
    ticks = filled_rows // 2

    # Detect GAME_OVER: if bar is full (filled_rows >= 64) the game is over.
    # Actually E15: after 57 actions bar was at rows 0..63 (full, 64 rows) and
    # next action gave GAME_OVER. So when bar full, state is GAME_OVER.
    game_over = filled_rows >= 64

    # Block positions
    blocks = {
        (49, 29): 'e',
        (49, 34): 'e',
        (54, 29): 'e',
        (54, 24): 'e',
        (59, 34): 'e',
        (59, 24): 'e',
    }
    # Replay history to get block states (toggle on click within block)
    for a in history:
        m = re.match(r"CLICK\s+(\d+)\s+(\d+)", a)
        if m:
            x, y = int(m.group(1)), int(m.group(2))
            for (br, bc) in blocks:
                if br <= x < br + 3 and bc <= y < bc + 3:
                    cur = blocks[(br, bc)]
                    # cycle e->0->2->e ; but observed e->0->e mostly. Use e->0->2->e
                    if cur == 'e':
                        blocks[(br, bc)] = '0'
                    elif cur == '0':
                        blocks[(br, bc)] = '2'
                    elif cur == '2':
                        blocks[(br, bc)] = 'e'
                    break

    # Sync block cells to grid from current frame? The frame already shows them.
    # We'll trust frame for current state; blocks dict is for predicting toggles.

    # --- Dial model ---
    # The dial is a 4-row band (rows 19-22) with a pattern of 9/a/2 that shifts.
    # We model it as: a 2x2 '9' block and a 2x2 'a' block, plus optional '2' fill.
    # ACTION1: shift pattern left by 2, swap 9<->a in the pair.
    # ACTION3: shift left by 4, produce wide '2' band.
    # ACTION4: set wide pattern.
    # This is approximate. We'll track a "dial_col" (left edge of 9-pair) and phase.
    # From E12/E13/E14: the 9-pair moves left: c39->c37->c33->c29->c25->c23...
    # Each ACTION1 moves the 9-pair left by 2 and swaps which is 9 vs a.
    # ACTION3 moves left by 4 and adds '2' band.
    # We'll just track the last dial state from history by replaying ACTIONs.

    # Dial state: (col_of_9_pair_left, which_is_9) where pair is 2 cols wide.
    # Initialize from frame: find leftmost '9' in row 19.
    dial_col = None
    dial_9_left = True
    for c in range(64):
        if get_cell(19, c) == '9':
            dial_col = c
            break
    if dial_col is None:
        dial_col = 35  # default

    # Replay ACTIONs to update dial_col (approximate)
    for a in history:
        if a == "ACTION1":
            dial_col -= 2
            dial_9_left = not dial_9_left
        elif a == "ACTION3":
            dial_col -= 4
            dial_9_left = not dial_9_left
        elif a == "ACTION4":
            dial_col -= 0  # ACTION4 sets wide pattern, keep col
        # ACTION2: unknown, treat as no shift

    # --- Apply probe actions ---
    steps = []
    for action in actions:
        changes = {}

        if game_over:
            # Only RESET works; other actions do nothing
            if action == "RESET":
                # Reset: clear bar, reset blocks, reset dial. We don't know exact
                # initial state, so just clear bar and mark not game over.
                for r in range(64):
                    for c in (62, 63):
                        if get_cell(r, c) == '0':
                            changes[f"{r},{c}"] = '5'
                            set_cell(r, c, '5')
                game_over = False
                ticks = 0
            steps.append({"changes": changes, "levels": 0, "state": "GAME_OVER" if game_over else "NOT_FINISHED"})
            continue

        if action.startswith("ACTION"):
            ticks += 1
            # Advance bar by 2 rows
            for i in range(ticks * 2):
                if i < 64:
                    if get_cell(i, 62) != '0':
                        changes[f"{i},62"] = '0'
                        set_cell(i, 62, '0')
                    if get_cell(i, 63) != '0':
                        changes[f"{i},63"] = '0'
                        set_cell(i, 63, '0')
            # Dial changes
            if action == "ACTION1":
                dial_col -= 2
                dial_9_left = not dial_9_left
            elif action == "ACTION3":
                dial_col -= 4
                dial_9_left = not dial_9_left
            elif action == "ACTION4":
                pass
            # Draw dial: 2x2 9 and 2x2 a at dial_col
            # Clear old dial region rows 19-22 cols 20-45 to '5'? Risky. Skip clearing.
            # Set 9 pair and a pair
            c9 = dial_col
            ca = dial_col + 2
            if not dial_9_left:
                c9, ca = ca, c9
            for r in range(19, 23):
                for dc in range(2):
                    if 0 <= c9 + dc < 64:
                        if get_cell(r, c9 + dc) != '9':
                            changes[f"{r},{c9+dc}"] = '9'
                            set_cell(r, c9 + dc, '9')
                    if 0 <= ca + dc < 64:
                        if get_cell(r, ca + dc) != 'a':
                            changes[f"{r},{ca+dc}"] = 'a'
                            set_cell(r, ca + dc, 'a')
            # Check game over
            if ticks * 2 >= 64:
                game_over = True

        elif action.startswith("CLICK"):
            m = re.match(r"CLICK\s+(\d+)\s+(\d+)", action)
            if m:
                x, y = int(m.group(1)), int(m.group(2))
                clicked_block = None
                for (br, bc) in blocks:
                    if br <= x < br + 3 and bc <= y < bc + 3:
                        clicked_block = (br, bc)
                        break
                if clicked_block:
                    cur = blocks[clicked_block]
                    if cur == 'e':
                        new = '0'
                    elif cur == '0':
                        new = '2'
                    elif cur == '2':
                        new = 'e'
                    else:
                        new = 'e'
                    blocks[clicked_block] = new
                    for dr in range(3):
                        for dc in range(3):
                            r, c = clicked_block[0] + dr, clicked_block[1] + dc
                            if get_cell(r, c) != new:
                                changes[f"{r},{c}"] = new
                                set_cell(r, c, new)
                    # Click on block advances bar
                    ticks += 1
                    for i in range(ticks * 2):
                        if i < 64:
                            if get_cell(i, 62) != '0':
                                changes[f"{i},62"] = '0'
                                set_cell(i, 62, '0')
                            if get_cell(i, 63) != '0':
                                changes[f"{i},63"] = '0'
                                set_cell(i, 63, '0')
                    if ticks * 2 >= 64:
                        game_over = True
                # else: background click, no change

        # Goal guess: level completes when dial is aligned. We don't know target,
        # so we never predict WIN here (mark "?"). This avoids false WIN predictions.
        levels = 0
        state = "GAME_OVER" if game_over else "NOT_FINISHED"
        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
