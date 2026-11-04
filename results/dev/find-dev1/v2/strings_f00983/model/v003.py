def predict(probe):
    # Each character's codepoint is shifted by +8 [E1, E2, E3]
    # Empty string stays empty [E1]
    # If any character's codepoint+8 exceeds U+10FFFF, output is "ERROR: ValueError" [E4]
    # Backslash is NOT special generally: it shifts like any other char [E10]
    # Exception: a 't' immediately following a backslash is dropped (backslash still shifts) [E9, E10]
    out = []
    for s in probe.get("inputs", []):
        try:
            shifted = []
            err = False
            prev = None
            for c in s:
                if c == 't' and prev == '\\':
                    prev = c
                    continue
                n = ord(c) + 8
                if n > 0x10FFFF:
                    err = True
                    break
                shifted.append(chr(n))
                prev = c
            out.append("ERROR: ValueError" if err else "".join(shifted))
        except Exception:
            out.append("ERROR: ValueError")
    return {"outputs": out}
