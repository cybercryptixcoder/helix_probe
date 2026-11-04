def predict(probe):
    # First char: letter a-y/A-Y -> +2; z/Z or non-letter -> +4 [E1,E2,E4,E6,E8,E10,E11]
    # All other chars -> +4 [E1,E4,E5,E7,E9,E11]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'y') or ('A' <= c <= 'Y')):
                sh = 2
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
