def predict(probe):
    # Each character's code point is shifted +8 [E1, E2, E3, E4]
    # No wraparound at 128 or within classes; plain ord(c)+8 [E2]
    # Applies per Unicode code point, including astral chars [E4]
    # If any character's shifted code point exceeds 0x10FFFF, the whole
    #   call raises ValueError (box returns "ERROR: ValueError") [E5]
    #   e.g. U+10FFFF (max) -> 0x110007 > 0x10FFFF -> error [E5]
    # Surrogate halves are shifted as individual code points [E4, E5]
    def shift(s):
        out = []
        for c in s:
            n = ord(c) + 8
            if n > 0x10FFFF:
                raise ValueError("chr() arg not in range(0x110000)")
            out.append(chr(n))
        return ''.join(out)

    results = []
    for x in probe["inputs"]:
        try:
            results.append(shift(x))
        except ValueError:
            results.append("ERROR: ValueError")
    return {"outputs": results}
