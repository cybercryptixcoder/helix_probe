def predict(probe):
    # Each character's code point is shifted by +8 [E1: 'abc123'->'ijk9:;', 'level'->'tm~mt', 'Zebra'->'bmjzi']
    # Shift applies uniformly to all chars including digits, symbols, spaces, uppercase [E1]
    # 'Hello World function lazy' -> 'Pmttw(_wztl(n}vkqwv(ti\x82\x81' confirms +8 on space, uppercase, lowercase
    # 'bananaUPPER' -> 'jivivi]XXMZ' confirms +8 on uppercase
    # ' Zebralower' -> '(bmjzitw\x7fmz' confirms +8 on leading space and lowercase
    return {"outputs": ["".join(chr(ord(c) + 8) for c in s) for s in probe["inputs"]]}
