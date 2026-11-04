def predict(probe):
    # Counter: rows 0..63 cols 62-63, one 2-row band per advance [E1-E11]
    # Advance: capable action (ACTION1/3/4, CLICK x in 25/30/35) advances
    #   unless same as previous capable action AND that one advanced [E1-E11]
    # First action of level is a full no-op [E1]
    # Puzzle block rows 19-22 cols 35-42: 2 row-blocks x 4 col-tiles (2x2).
    #   ACTION4 reverses the 4 col-tiles [E11]. ACTION1/2/3: unknown, no change (?)
    # Target blocks: CLICK x in {25,30,35} lights 3x3 at (y-1..y+1, x-1..x+1)
    #   colour by per-block click parity: even->e, odd->0 (x=30,y=55 odd->2) [E1-E11]
    # GOAL (?): filling all 32 counter bands completes level 1
    actions = probe.get("actions", [])
    frame = probe.get("frame")
    history = list(probe.get("history", []) or [])

    def count_bands(fr):
        if not fr: return 0
        n = 0
        for k in range(32):
            r = 2*k
            if r < len(fr) and len(fr[r])>63 and fr[r][62]=='0' and fr[r][63]=='0':
                n += 1
            else: break
        return n

    def parse_click(a):
        try:
            p=a.split(); return int(p[1]),int(p[2])
        except Exception: return None,None

    def is_capable(a):
        if not isinstance(a,str): return False
        if a in ("ACTION1","ACTION3","ACTION4"): return True
        if a.startswith("CLICK"):
            x,_=parse_click(a); return x in (25,30,35)
        return False

    last_cap=None; last_cap_adv=False
    for i,a in enumerate(history):
        if not is_capable(a): continue
        if i==0:
            last_cap=a; last_cap_adv=False; continue
        if a==last_cap and last_cap_adv: last_cap_adv=False
        else: last_cap_adv=True
        last_cap=a

    bands=count_bands(frame)
    steps=[]
    for idx,a in enumerate(actions):
        changes={}
        first=(len(history)==0 and idx==0)
        adv=False
        if is_capable(a) and bands<32 and not first:
            if a==last_cap and last_cap_adv: adv=False
            else: adv=True
        if adv:
            r=2*bands
            for dr in (0,1):
                for c in (62,63): changes["%d,%d"%(r+dr,c)]='0'
            bands+=1; last_cap_adv=True
        else:
            if is_capable(a): last_cap_adv=False
        if is_capable(a): last_cap=a

        # Puzzle: ACTION4 reverses 4 col-tiles in both row-blocks [E11]
        if a=="ACTION4" and frame:
            for rb in (19,21):
                tiles=[]
                for ct in (35,37,39,41):
                    try: tiles.append(frame[rb][ct])
                    except Exception: tiles.append('?')
                rev=tiles[::-1]
                for j,ct in enumerate((35,37,39,41)):
                    for rr in (rb,rb+1):
                        for cc in (ct,ct+1):
                            changes["%d,%d"%(rr,cc)]=rev[j]

        # Target block on CLICK x in {25,30,35}, unless first action
        if isinstance(a,str) and a.startswith("CLICK") and not first:
            x,y=parse_click(a)
            if x in (25,30,35):
                r0=y-1
                cols=(29,30,31) if x==30 else ((34,35,36) if x==35 else (24,25,26))
                cnt=0
                for h in history:
                    if isinstance(h,str) and h.startswith("CLICK"):
                        hx,hy=parse_click(h)
                        if hx==x and hy is not None and (hy-1)==r0: cnt+=1
                for j in range(idx):
                    pa=actions[j]
                    if isinstance(pa,str) and pa.startswith("CLICK"):
                        px,py=parse_click(pa)
                        if px==x and py is not None and (py-1)==r0: cnt+=1
                col='e' if cnt%2==0 else ('2' if (x==30 and y==55) else '0')
                for rr in (r0,r0+1,r0+2):
                    for cc in cols: changes["%d,%d"%(rr,cc)]=col

        lv = 1 if bands>=32 else 0
        st = "WIN" if lv else "NOT_FINISHED"
        steps.append({"changes":changes,"levels":lv,"state":st})
    return {"steps":steps}
