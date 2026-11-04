def predict(probe):
    # Each character's codepoint is shifted by +8 [E1, E2, E3]
    # Empty string stays empty [E1]
    # If any character's codepoint+8 exceeds U+10FFFF, output is "ERROR: ValueError" [E4]
    out = []
    for s in probe.get("inputs", []):
        try:
            shifted = []
            err = False
            for c in s:
                n = ord(c) + 8
                if n > 0x10FFFF:
                    err = True
                    break
                shifted.append(chr(n))
            out.append("ERROR: ValueError" if err else "".join(shifted))
        except Exception:
            out.append("ERROR: ValueError")
    return {"outputs": out}
