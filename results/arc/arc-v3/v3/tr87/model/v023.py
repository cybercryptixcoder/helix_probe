def predict(probe):
    # Beliefs:
    # - Screen is 64x64. Rows 0-33 bg=2, rows 34-63 bg=3 [screen].
    # - Top cards (rows 4-10,13-19,22-28) show target patterns in 5/7 with border a [screen].
    # - Bottom cards (rows 41-47) show current patterns in 5/7 with border a [screen].
    # - ACTION1/ACTION2 toggle a card's interior between two patterns [E2,E21,E24].
    # - ACTION3/ACTION4 move a selection highlight among top cards, toggling 3<->0 in 5-wide blocks [E1,E7].
    # - A '4' counter at row63 moves left per toggle action; at c0 -> GAME_OVER [E32].
    # - RESET restores level and counter [E33,E38].
    # - Goal (?): bottom cards match top target cards -> WIN.
    # ? Exact toggle target & matching rule uncertain; best guess below.

    grid = [list(row) for row in probe["frame"]]
    history = list(probe.get("history", []))
    actions = probe.get("actions", [])
    level = probe.get("level", 0)

    def find_counter(grid):
        # find '4' in row 63
        row = grid[63]
        for c in range(63, -1, -1):
            if row[c] == '4':
                return c
        return None

    def bottom_matches_top(grid):
        # compare bottom card interiors (rows 42-46) to top card interiors (rows 5-9 etc.)
        # ? guess: compare first bottom card block to first top card block
        # top cards at cols 12-18,21-27,30-36,39-45 (rows 4-10 etc.)
        # bottom cards at cols 14-52 (rows 41-47)
        # Simplify: compare the pattern region rows 42-46 cols 15-52 vs top rows 5-9
        # We'll check if bottom row-42..46 interiors equal corresponding top patterns.
        # Placeholder: compare bottom card at cols 15-18 to top card at 15-18
        # (uncertain)
        return False

    def toggle_card(grid, r0, c0):
        # toggle interior 5<->7 in a 5x5 region starting r0+1,c0+1
        for r in range(r0+1, r0+6):
            for c in range(c0+1, c0+6):
                if grid[r][c] == '5':
                    grid[r][c] = '7'
                elif grid[r][c] == '7':
                    grid[r][c] = '5'

    steps = []
    state = "NOT_FINISHED"
    levels_done = 0

    # determine which card ACTION1/ACTION2 toggles: the "active" card
    # ? assume it's the card at rows 52-56 (bottom card region rows 52-56)
    # Actually bottom cards are at rows 41-47; rows 52-56 is a separate card row.
    # From evidence, ACTION1/ACTION2 change rows 52-56 -> that's the toggle target.
    # So there are cards at rows 52-56 too (cols 15-19,22-26,29-33,36-40,43-47).

    for act in actions:
        changes = {}
        if state == "GAME_OVER":
            if act == "RESET":
                # reset: restore level; approximate by re-reading? we can't know original.
                # We'll just clear counter to c63 and mark not finished.
                # ? best effort
                grid[63] = ['1']*63 + ['4']
                state = "NOT_FINISHED"
            steps.append({"changes": {}, "levels": levels_done, "state": state})
            continue

        if act == "RESET":
            grid[63] = ['1']*63 + ['4']
            state = "NOT_FINISHED"
            steps.append({"changes": {}, "levels": levels_done, "state": state})
            continue

        if act in ("ACTION1", "ACTION2"):
            # toggle the card at rows 52-56, cols 22-26 region (the "active" card)
            # ? which card? evidence shows changes around cols 15-47 in rows 52-56.
            # The active card seems to be the one near the counter position.
            cpos = find_counter(grid)
            # map counter position to a card column
            # cards at cols 15-19,22-26,29-33,36-40,43-47
            card_cols = [15,22,29,36,43]
            # pick card nearest to some function of counter
            # ? guess: active card index = (63 - cpos) % 5 ... uncertain
            idx = 0
            if cpos is not None:
                idx = ((63 - cpos) // 7) % 5
            c0 = card_cols[idx]
            r0 = 52
            before = {}
            for r in range(r0, r0+5):
                for c in range(c0, c0+5):
                    before[(r,c)] = grid[r][c]
            toggle_card(grid, r0-1, c0-1)
            for r in range(r0, r0+5):
                for c in range(c0, c0+5):
                    if grid[r][c] != before[(r,c)]:
                        changes[f"{r},{c}"] = grid[r][c]
            # decrement counter
            if cpos is not None and cpos > 0:
                grid[63][cpos] = '1'
                grid[63][cpos-1] = '4'
            elif cpos == 0:
                state = "GAME_OVER"
        elif act in ("ACTION3", "ACTION4"):
            # move selection among top cards; toggle 3<->0 in 5-wide blocks
            # find current '0' block in rows 48-49
            # ? simplified: toggle a block
            pass

        if bottom_matches_top(grid):
            levels_done += 1
            state = "WIN"

        steps.append({"changes": changes, "levels": levels_done, "state": state})

    return {"steps": steps}
