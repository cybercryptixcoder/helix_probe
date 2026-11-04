def predict(probe):
    # Beliefs (evidence):
    # - 5 tiles at interior cols 15,22,29,36,43; interiors rows 52-56 (5x5), cells are 5/7 [E24,E25]
    # - Region markers at r48-49, r59-60 over each tile: '3'=active, '0'=inactive [E22,E26,E27]
    # - ACTION4 moves active tile right, ACTION3 moves it left [E26,E27,E22]
    # - ACTION1/ACTION2 toggle a fixed 11-cell subset of the active tile's interior (5<->7) [E24,E25]
    # - r63 is a progress bar filled from the right with '4'; fully filled => GAME_OVER (loss) [E32]
    # - RESET restores r63 to '1' and clears active marker [E33]
    # - GOAL (guess "?"): make all 5 tile interiors uniform (all 5 or all 7) -> WIN
    screen = [list(row) for row in probe["frame"]]
    actions = probe["actions"]

    TILES = [15, 22, 29, 36, 43]
    # fixed toggle subset (relative to tile top-left at r52,c=L), from E24/E25
    PATTERN = [(0,4),(1,0),(1,3),(1,4),(2,1),(2,2),(2,3),(3,0),(3,1),(3,4),(4,0)]

    def find_selected(scr):
        for i, L in enumerate(TILES):
            if scr[48][L] == '3':
                return i
        return 0

    def count_filled(scr):
        return scr[63].count('4')

    def all_uniform(scr):
        for L in TILES:
            vals = set()
            for dr in range(5):
                for dc in range(5):
                    vals.add(scr[52+dr][L+dc])
            if len(vals) != 1:
                return False
        return True

    sel = find_selected(screen)
    filled = count_filled(screen)

    def move_markers(scr, changes, oldL, newL):
        for r in (48,49,59,60):
            for c in range(oldL, oldL+5):
                if scr[r][c] == '3':
                    changes[f"{r},{c}"] = '0'; scr[r][c] = '0'
        for r in (48,49,59,60):
            for c in range(newL, newL+5):
                if scr[r][c] == '0':
                    changes[f"{r},{c}"] = '3'; scr[r][c] = '3'

    steps = []
    for act in actions:
        changes = {}
        state = "NOT_FINISHED"
        levels = 0
        if act == 'ACTION4':
            ns = min(sel+1, len(TILES)-1)
            if ns != sel:
                move_markers(screen, changes, TILES[sel], TILES[ns])
                sel = ns
        elif act == 'ACTION3':
            ns = max(sel-1, 0)
            if ns != sel:
                move_markers(screen, changes, TILES[sel], TILES[ns])
                sel = ns
        elif act in ('ACTION1','ACTION2'):
            L = TILES[sel]
            for (dr,dc) in PATTERN:
                r = 52+dr; c = L+dc
                old = screen[r][c]
                new = '7' if old == '5' else '5'
                changes[f"{r},{c}"] = new
                screen[r][c] = new
            # advance cursor (best guess: every productive toggle advances)
            if filled < 64:
                col = 63 - filled
                changes[f"63,{col}"] = '4'
                screen[63][col] = '4'
                filled += 1
                if filled >= 64:
                    state = "GAME_OVER"
        elif act == 'RESET':
            for c in range(64):
                if screen[63][c] == '4':
                    changes[f"63,{c}"] = '1'; screen[63][c] = '1'
            filled = 0
            # clear active marker to tile 0
            if sel != 0:
                move_markers(screen, changes, TILES[sel], TILES[0])
                sel = 0
        # goal guess "?": all tile interiors uniform
        if state == "NOT_FINISHED" and all_uniform(screen):
            state = "WIN"; levels = 1
        steps.append({"changes":changes,"levels":levels,"state":state})
    return {"steps":steps}
