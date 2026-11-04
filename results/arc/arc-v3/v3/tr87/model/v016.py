def predict(probe):
    screen = probe["frame"]
    history = probe.get("history", [])
    actions = probe["actions"]
    level = probe.get("level", 0)
    
    # current filled count in row 63 (color '4' from right)
    row63 = screen[63]
    # count cells that are '4'
    filled = row63.count('4')
    # unfilled cells are those not '4' (the '1's on left)
    
    # cumulative counts from history
    cnt = {'ACTION1':0,'ACTION2':0,'ACTION3':0,'ACTION4':0}
    for a in history:
        if a in cnt: cnt[a]+=1
    
    steps=[]
    for act in actions:
        changes={}
        state="NOT_FINISHED"
        levels=0
        if act in cnt:
            cnt[act]+=1
            c=cnt[act]
            productive=False
            if act=='ACTION1' and c%2==1: productive=True
            elif act=='ACTION2' and c%2==1: productive=True
            elif act=='ACTION4' and c%2==0: productive=True
            elif act=='ACTION3' and c%2==1: productive=True  # ?
            if productive and filled<64:
                # fill rightmost unfilled cell
                # find rightmost cell that is not '4'
                for col in range(63,-1,-1):
                    if row63[col]!='4':
                        # this is the rightmost unfilled? Actually fill from right.
                        pass
                # simpler: filled increases, the cell at column (63-filled) becomes 4
                col = 63 - filled
                if col>=0:
                    changes[f"63,{col}"]='4'
                    filled+=1
                if filled>=64:
                    levels=1
                    state="WIN"
        steps.append({"changes":changes,"levels":levels,"state":state})
        if state=="WIN":
            # subsequent steps? keep WIN
            pass
    return {"steps":steps}
