def predict(probe):
    # First char: letter a-v/A-V -> +2; w,x,y,z (any case) or non-letter -> +4
    #   [E8: a,b,c,A,B,C -> +2; E10: V,W -> +2, X,Y -> +4; E12: u,v -> +2, w,x,y -> +4;
    #    E2: z,Z -> +4; E6: y,Y -> +4]
    # All other chars -> +4 [E1,E4,E5,E7,E9,E11]
    # So the +2 region is letters 'a'..'v' and 'A'..'V'; everything else +4.
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'v') or ('A' <= c <= 'V')):
                sh = 2
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
