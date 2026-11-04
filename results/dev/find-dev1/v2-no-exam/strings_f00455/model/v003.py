def predict(probe):
    # Each Unicode code point is incremented by 1 [E1, E2, E3, E4]
    # Works per code point, not per UTF-16 unit: emoji/CJK shift as single units [E3, E4, E5]
    # Lone surrogates are shifted as ordinary code points [E5: \ud800->\ud801, \udc00->\udc01]
    # \uffff -> \ud800\udc00 (i.e. 0xFFFF+1 = 0x10000) [E4, E5]
    # If any result exceeds 0x10FFFF, the whole call errors with ValueError [E5: \udbff\udfff]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for c in s:
            cp = ord(c) + 1
            if cp > 0x10FFFF:
                return {"outputs": ["ERROR: ValueError"] * len(probe.get("inputs", []))}
            r.append(chr(cp))
        out.append(''.join(r))
    return {"outputs": out}
