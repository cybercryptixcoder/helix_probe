def predict(probe):
    frame = probe.get("frame")
    actions = probe.get("actions", []) or []
    level = probe.get("level", 0)
    history = probe.get("history", []) or []
    grid = [list(row) for row in frame] if frame else [['5']*64 for _ in range(64)]
    
    def bar_fill(g):
        n=0
        for c in range(63,-1,-1):
            if g[63][c]=='5': n+=1
            else: break
        return n
    def clear_bar(g,ch):
        for c in range(64):
            if g[63][c]!='4':
                ch[f"63,{c}"]='4'; g[63][c]='4'
    def toggle_r7(g,ch):
        seg=[g[7][c] for c in range(35,46)]
        isA=(seg[0:5]==['0']*5 and seg[6:11]==['3']*5)
        newA,newB=('3','0') if isA else ('0','3')
        for c in range(35,40):
            if g[7][c]!=newA: ch[f"7,{c}"]=newA; g[7][c]=newA
        for c in range(41,46):
            if g[7][c]!=newB: ch[f"7,{c}"]=newB; g[7][c]=newB
    
    # replay history
    counts={}
    prev_act=None
    for h in history:
        h=h.strip()
        if h=="RESET":
            counts={}; prev_act=None
        elif h.startswith("CLICK"):
            p=h.split()
            try: t=(int(p[1]),int(p[2]))
            except: t=None
            if t: counts[t]=counts.get(t,0)+1
            prev_act=h
        elif h.startswith("ACTION"):
            prev_act=h
    
    steps=[]; state="NOT_FINISHED"; levels=level
    def advance(g,ch):
        fill=bar_fill(g)
        if fill<64:
            col=63-fill
            if g[63][col]!='5':
                ch[f"63,{col}"]='5'; g[63][col]='5'; return True
        return False
    
    for act in actions:
        ch={}; act=act.strip()
        if state=="GAME_OVER":
            if act=="RESET":
                clear_bar(grid,ch); state="NOT_FINISHED"; counts={}; prev_act=None
            steps.append({"changes":ch,"levels":levels,"state":state}); continue
        if act=="RESET":
            clear_bar(grid,ch); state="NOT_FINISHED"; counts={}; prev_act=None
            steps.append({"changes":ch,"levels":levels,"state":state}); continue
        
        if act.startswith("CLICK"):
            p=act.split()
            try: x=int(p[1]); y=int(p[2])
            except: x=y=-1
            if (x,y) in ((43,4),(37,4)):
                toggle_r7(grid,ch)
            t=(x,y)
            counts[t]=counts.get(t,0)+1
            if counts[t]%2==0:
                advance(grid,ch)
        else:
            if prev_act!=act:
                advance(grid,ch)
        
        fill=bar_fill(grid)
        if fill>=64: state="GAME_OVER"
        prev_act=act
        steps.append({"changes":ch,"levels":levels,"state":state})
    return {"steps":steps}
