def predict(probe):
    # Case transform: first char uppercased, rest lowercased [E1, E2]
    #   "HELLO"->"Hello", "aBcDeF"->"Abcdef", "McDonald"->"Mcdonald" [E1,E2]
    # Insert "10" at position len(s)//2 (floor) of the ORIGINAL string [E1,E3]
    #   len 5 -> pos 2, len 6 -> pos 3, len 1 -> pos 0, len 0 -> pos 0 [E1,E3]
    # BUT single-character inputs are NOT case-transformed: "a"->"10a", "Z"->"10z" [E3]
    #   i.e. lone char is lowercased, not uppercased. [E3]
    #   "x"->"10x" [E1] consistent (already lower). "Z"->"10z" shows lowercasing.
    # So for len==1: lowercase the char. For len>=2: first upper, rest lower. [E3]
    out = []
    for s in probe.get("inputs", []):
        if len(s) == 1:
            t = s.lower()
        elif s:
            t = s[0].upper() + s[1:].lower()
        else:
            t = s
        p = len(s) // 2
        out.append(t[:p] + "10" + t[p:])
    return {"outputs": out}
