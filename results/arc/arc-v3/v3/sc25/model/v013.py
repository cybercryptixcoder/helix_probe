def predict(probe):
    # Model of the black box (v13).
    #
    # Beliefs (from evidence):
    # - Grid 64x64 of hex digits; background '5'.
    # - Right-edge bar (cols 62-63) is a TIMER: fills 2 rows per "tick" from row 0,
    #   colour '0'. A tick = any ACTION, or any CLICK that hits a block [E1..E18].
    #   When bar reaches bottom (row 62-63 filled), the NEXT tick => GAME_OVER [E14,E15].
    # - RESET restores the level to its INITIAL state [E16]:
    #     bar cols 62-63 all 'e' (rows 0-63),
    #     dial: rows 19-22, cols 23-26 = '2', cols 39-40 = '9', cols 41-42 = 'a',
    #     blocks back to initial 'e' pattern.
    # - Blocks are 3x3 objects. Clicking one cycles its colour e->0->e (2-state!) [E18].
    #   E18: click1 e->e (no change!), click2 e->0, click3 0->e, click4 e->0.
    #   Wait: E18 shows click1 = e (no change), click2 = 0, click3 = e, click4 = 0.
    #   So cycle is e->e? No: click1 changed nothing (already e), click2 ->0, click3->e, click4->0.
    #   Actually E18 first click shows "9 cells changed ... :e" meaning it SET to e (was already e?).
    #   The block at (49,29) starts 'e'. Click1: changes to e (no visible change but listed).
    #   Hmm the changes list shows r49-51 c29-31:e on click1 — that means it was NOT e before.
    #   So initial block colour is NOT e. Let's reconsider: click1 sets to e, click2 sets to 0,
    #   click3 sets to e, click4 sets to 0. So cycle is e<->0 (2-state), and initial was 0 or 2.
    #   From E8: click1 ->0, click2 ->e, click3 ->0. So sequence 0,e,0 => cycle e<->0, start e.
    #   E18: click1->e, click2->0, click3->e, click4->0 => start was 0 (click1 0->e).
    #   So block (49,29) initial colour after E16 RESET is '0'? But E16 fresh... 
    #   Actually E18 ran "after:1" i.e. 1 action since level began. So block already clicked once?
    #   No — after:1 means 1 action used. The block state at start of E18: unknown.
    #   Simplest consistent rule: clicking a block toggles e<->0. [E8,E18]
    #   Clicking background (no block) does nothing [E6,E9,E11,E17].
    #   A block click also advances the bar by one tick [E1..E18].
    # - ACTION1: dial shifts; sets 2x2 '9' and 2x2 'a' pair, swapping sides each ACTION1,
    #   pair moves LEFT by 2 cols per ACTION1. Observed 9-pair left edge:
    #   39 -> 37 -> 33 -> 31 -> 27 -> 25 -> 23 ... [E2,E4,E10,E12,E13,E14].
    #   ACTION1 also advances bar by one tick.
    # - ACTION3: same as ACTION1 but shifts left by 4 and paints a '2' band
    #   cols (X+4..X+7) on rows 19-22 [E6,E10,E12,E13,E14]. Advances bar by one tick.
    # - ACTION4: sets fixed wide pattern: cols 35-38='2', 39-40='a', 41-42='9'
    #   on rows 19-22 [E7,E11]. Advances bar by one tick.
    # - ACTION2: no visible effect observed [E2,E4]; still advances bar by one tick.
    # - GAME_OVER: only RESET works; other actions do nothing [E15].
    #
    # GOAL (best guess, "?"): The dial must be aligned to a target configuration
    # before the bar runs out. We do NOT know the exact target. We never predict WIN
    # here (marked "?"); the box will correct us.

    import re

    actions = probe.get("actions", [])
    frame = probe.get("frame", None)

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
    filled_rows = 0
    for r in range(64):
        if get_cell(r, 62) == '0':
            filled_rows += 1
        else:
            break
    ticks = filled_rows // 2
    game_over = filled_rows >= 64

    # Block positions (3x3 top-left corners).
    block_tops = [(49, 29), (49, 34), (54, 29), (54, 24), (59, 34), (59, 24)]
    blocks = {}
    for (br, bc) in block_tops:
        blocks[(br, bc)] = get_cell(br, bc)

    def toggle(col):
        # e<->0 cycle [E8,E18]
        if col == 'e':
            return '0'
        if col == '0':
            return 'e'
        if col == '2':
            return 'e'
        return 'e'

    def find_block(x, y):
        for (br, bc) in block_tops:
            if br <= x < br + 3 and bc <= y < bc + 3:
                return (br, bc)
        return None

    def advance_bar(changes):
        nonlocal ticks, game_over
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

    # --- Dial state ---
    dial_col = None
    for c in range(64):
        if get_cell(19, c) == '9':
            dial_col = c
            break
    if dial_col is None:
        dial_col = 39
    dial_9_left = True
    if get_cell(19, dial_col) == '9' and get_cell(19, dial_col + 2) == 'a':
        dial_9_left = True
    elif get_cell(19, dial_col) == 'a' and get_cell(19, dial_col + 2) == '9':
        dial_9_left = False

    def paint_dial(changes, c9, ca, extra2=None):
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
            if extra2 is not None:
                for c in extra2:
                    if 0 <= c < 64:
                        if get_cell(r, c) != '2':
                            changes[f"{r},{c}"] = '2'
                            set_cell(r, c, '2')

    steps = []
    for action in actions:
        changes = {}

        if game_over:
            if action == "RESET":
                for r in range(64):
                    for c in (62, 63):
                        if get_cell(r, c) != 'e':
                            changes[f"{r},{c}"] = 'e'
                            set_cell(r, c, 'e')
                for r in range(19, 23):
                    for c in range(23, 27):
                        if get_cell(r, c) != '2':
                            changes[f"{r},{c}"] = '2'
                            set_cell(r, c, '2')
                    for c in (39, 40):
                        if get_cell(r, c) != '9':
                            changes[f"{r},{c}"] = '9'
                            set_cell(r, c, '9')
                    for c in (41, 42):
                        if get_cell(r, c) != 'a':
                            changes[f"{r},{c}"] = 'a'
                            set_cell(r, c, 'a')
                game_over = False
                ticks = 0
                dial_col = 39
                dial_9_left = True
            steps.append({"changes": changes, "levels": 0,
                          "state": "GAME_OVER" if game_over else "NOT_FINISHED"})
            continue

        if action.startswith("ACTION"):
            if action == "ACTION1":
                dial_col -= 2
                dial_9_left = not dial_9_left
                c9 = dial_col if dial_9_left else dial_col + 2
                ca = dial_col + 2 if dial_9_left else dial_col
                paint_dial(changes, c9, ca)
            elif action == "ACTION3":
                dial_col -= 4
                dial_9_left = not dial_9_left
                c9 = dial_col if dial_9_left else dial_col + 2
                ca = dial_col + 2 if dial_9_left else dial_col
                extra2 = list(range(dial_col + 4, dial_col + 8))
                paint_dial(changes, c9, ca, extra2)
            elif action == "ACTION4":
                for r in range(19, 23):
                    for c in range(35, 39):
                        if get_cell(r, c) != '2':
                            changes[f"{r},{c}"] = '2'
                            set_cell(r, c, '2')
                    for c in (39, 40):
                        if get_cell(r, c) != 'a':
                            changes[f"{r},{c}"] = 'a'
                            set_cell(r, c, 'a')
                    for c in (41, 42):
                        if get_cell(r, c) != '9':
                            changes[f"{r},{c}"] = '9'
                            set_cell(r, c, '9')
                dial_col = 39
                dial_9_left = False
            advance_bar(changes)

        elif action.startswith("CLICK"):
            m = re.match(r"CLICK\s+(\d+)\s+(\d+)", action)
            if m:
                x, y = int(m.group(1)), int(m.group(2))
                blk = find_block(x, y)
                if blk is not None:
                    cur = blocks.get(blk, get_cell(blk[0], blk[1]))
                    new = toggle(cur)
                    blocks[blk] = new
                    for dr in range(3):
                        for dc in range(3):
                            r, c = blk[0] + dr, blk[1] + dc
                            if get_cell(r, c) != new:
                                changes[f"{r},{c}"] = new
                                set_cell(r, c, new)
                    advance_bar(changes)

        levels = 0
        state = "GAME_OVER" if game_over else "NOT_FINISHED"
        steps.append({"changes": changes, "levels": levels, "state": state})

    return {"steps": steps}
