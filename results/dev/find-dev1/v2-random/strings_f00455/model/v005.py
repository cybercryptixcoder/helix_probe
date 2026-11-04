def predict(probe):
    # Each char shifted +1 in ord [E1-E8]
    # Original letters (a-z,A-Z): index 0 -> uppercase, else lowercase [E1,E3]
    # Non-letters: keep shifted char as-is (no case change) [E5 a!@# -> B"A$]
    # BUT: a leading space stays a space? No: ' Zebralower' -> '!{fcsbmpxfs' [E1]
    #   and '  xyz ' -> '!!yz{!' [E8], ' Zebra' -> '!{fcsb' [E8]
    #   So space at index 0 -> '!' (shifted), NOT uppercased (it's not a letter).
    # Wait: E1 ' Zebralower' -> '!{fcsbmpxfs': ' '->'!', 'Z'->'{' (lowercased after shift: '{').
    #   'Zebra' -> '[fcsb': 'Z'->'[' at index 0, uppercase of '[' is '['. OK.
    # E8 ' Zebra' -> '!{fcsb': ' '->'!', 'Z'->'{' (index1, lowercased). OK.
    # So rule: shift; if original is a letter, index0->upper else lower; else unchanged.
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            n = chr(ord(c) + 1)
            if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
                n = n.upper() if i == 0 else n.lower()
            r.append(n)
        out.append("".join(r))
    return {"outputs": out}
