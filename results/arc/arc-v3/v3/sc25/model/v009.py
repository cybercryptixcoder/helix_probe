def predict(probe):
    # Counter: rows 0..63 cols 62-63, one 2-row band per advance [E1-E12]
    # Advance: capable action (ACTION1/3/4, CLICK x in 25/30/35) advances
    #   unless same as previous capable action AND that one advanced [E1-E12]
    # First action of level is a full no-op [E1]
    # Puzzle block rows 19-22: 2 row-blocks x 4 col-tiles (2x2).
    #   ACTION4 reverses the 4 col-tiles [E11].
    #   ACTION1: rotates tiles right by 1 (cols shift +2), colours cycle 9/a/2 [E2,E12]
    #   ACTION3: rotates tiles left by 1 (cols shift -2), colours cycle 9/a/2 [E2,E12]
    #   ACTION2: unknown, appears no-op on puzzle (?) [E4]
    # Target blocks: CLICK x in {25,30,35} lights 3x3 at (y-1..y+1, x-1..x+1)
    #   colour by per-block click parity: even->e, odd->0 (x=30,y=55 odd->2) [E1-E12]
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

    # Puzzle state: 2 row-blocks x 4 col-tiles, each tile is a 2x2 colour.
    # Represent as list of 8 tile colours (rb0: c35,37,39,41; rb1: same).
    def read_puzzle(fr):
        if not fr: return None
        tiles=[]
        for rb in (19,21):
            for ct in (35,37,39,41):
                try: tiles.append(fr[rb][ct])
                except Exception: tiles.append('?')
        return tiles

    def write_puzzle(tiles, changes):
        for k,ct in enumerate((35,37,39,41)):
            for rr in (19,20):
                for cc in (ct,ct+1):
                    changes["%d,%d"%(rr,cc)]=tiles[k]
            for rr in (21,22):
                for cc in (ct,ct+1):
                    changes["%d,%d"%(rr,cc)]=tiles[4+k]

    # colour cycle for puzzle tiles: 9 -> a -> 2 -> 9 (guess from E2/E12)
    def next_col(c):
        return {'9':'a','a':'2','2':'9'}.get(c,c)

    bands=count_bands(frame)
    puzzle=read_puzzle(frame)
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

        # Puzzle transforms
        if puzzle is not None and not first:
            if a=="ACTION4":
                # reverse each row-block's 4 tiles
                newp = puzzle[0:4][::-1] + puzzle[4:8][::-1]
                write_puzzle(newp, changes); puzzle=newp
            elif a=="ACTION1":
                # rotate right by 1: last tile moves to front, colours cycle
                newp=[]
                for base in (0,4):
                    row=puzzle[base:base+4]
                    row=[next_col(c) for c in row]
                    row=[row[-1]]+row[:-1]
                    newp+=row
                write_puzzle(newp, changes); puzzle=newp
            elif a=="ACTION3":
                # rotate left by 1: first tile moves to end, colours cycle
                newp=[]
                for base in (0,4):
                    row=puzzle[base:base+4]
                    row=[next_col(c) for c in row]
                    row=row[1:]+[row[0]]
                    newp+=row
                write_puzzle(newp, changes); puzzle=newp

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
