def predict(probe):
    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = probe.get("history", [])
    
    grid = [list(row) for row in frame] if frame else [['2']*64 for _ in range(64)]
    
    sockets = [(15,19),(22,26),(29,33),(36,40),(43,47)]
    
    # Find active socket: the one with '0' at row 48
    active = None
    for i,(cs,ce) in enumerate(sockets):
        if grid[48][cs] == '0':
            active = i
            break
    if active is None:
        active = 0
    
    # Progress bar: find rightmost '4' in row 63
    prog = 63
    for c in range(63, -1, -1):
        if grid[63][c] == '4':
            prog = c
            break
    
    steps = []
    state = "NOT_FINISHED"
    levels_done = 0
    
    for a in actions:
        changes = {}
        if state == "GAME_OVER":
            if a == "RESET":
                prog = 63
                state = "NOT_FINISHED"
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue
        
        if a == "RESET":
            prog = 63
            # reset progress bar
            for c in range(64):
                if grid[63][c] == '4':
                    grid[63][c] = '1'
                    changes[f"63,{c}"] = '1'
            steps.append({"changes": changes, "levels": levels_done, "state": state})
            continue
        
        # progress bar moves left
        if prog > 0:
            old = prog
            prog -= 1
            if grid[63][prog] != '4':
                grid[63][prog] = '4'
                changes[f"63,{prog}"] = '4'
            if grid[63][old] == '4':
                grid[63][old] = '1'
                changes[f"63,{old}"] = '1'
            if prog == 0:
                state = "GAME_OVER"
        
        if a == "ACTION4":
            # active -> 3, next -> 0
            cs,ce = sockets[active]
            for r in (48,49,59,60):
                for c in range(cs,ce+1):
                    if r in (48,60) or c in (cs,ce):
                        if grid[r][c] in ('0','3'):
                            nv = '3'
                            if grid[r][c] != nv:
                                grid[r][c] = nv
                                changes[f"{r},{c}"] = nv
            nxt = (active+1)%5
            cs,ce = sockets[nxt]
            for r in (48,49,59,60):
                for c in range(cs,ce+1):
                    if r in (48,60) or c in (cs,ce):
                        if grid[r][c] in ('0','3'):
                            nv = '0'
                            if grid[r][c] != nv:
                                grid[r][c] = nv
                                changes[f"{r},{c}"] = nv
            active = nxt
        
        elif a == "ACTION3":
            cs,ce = sockets[active]
            for r in (48,49,59,60):
                for c in range(cs,ce+1):
                    if r in (48,60) or c in (cs,ce):
                        if grid[r][c] in ('0','3'):
                            nv = '3'
                            if grid[r][c] != nv:
                                grid[r][c] = nv
                                changes[f"{r},{c}"] = nv
            prv = (active-1)%5
            cs,ce = sockets[prv]
            for r in (48,49,59,60):
                for c in range(cs,ce+1):
                    if r in (48,60) or c in (cs,ce):
                        if grid[r][c] in ('0','3'):
                            nv = '0'
                            if grid[r][c] != nv:
                                grid[r][c] = nv
                                changes[f"{r},{c}"] = nv
            active = prv
        
        elif a in ("ACTION1","ACTION2"):
            # rotate 5x5 interior of active socket
            cs,ce = sockets[active]
            # interior rows 52-56, cols cs..ce (5x5)
            sub = [[grid[r][c] for c in range(cs,ce+1)] for r in range(52,57)]
            if a == "ACTION1":
                # rotate 90 CW
                new = [[sub[4-j][i] for j in range(5)] for i in range(5)]
            else:
                # rotate 90 CCW
                new = [[sub[j][4-i] for j in range(5)] for i in range(5)]
            for i in range(5):
                for j in range(5):
                    r = 52+i
                    c = cs+j
                    if grid[r][c] != new[i][j]:
                        grid[r][c] = new[i][j]
                        changes[f"{r},{c}"] = new[i][j]
        
        # GOAL guess: ? maybe all interiors match first interior
        steps.append({"changes": changes, "levels": levels_done, "state": state})
    
    return {"steps": steps}
