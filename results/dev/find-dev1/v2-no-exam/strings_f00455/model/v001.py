def predict(probe):
    # Caesar shift +1 on letters, preserving case [E1]
    # Non-letters (digits, spaces, punctuation) unchanged [E1]
    # 'z'->'a' and 'Z'->'A' wrap (assumed standard Caesar) [?]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for c in s:
            if 'a' <= c <= 'z':
                r.append(chr((ord(c) - ord('a') + 1) % 26 + ord('a')))
            elif 'A' <= c <= 'Z':
                r.append(chr((ord(c) - ord('A') + 1) % 26 + ord('A')))
            else:
                r.append(c)
        out.append(''.join(r))
    return {"outputs": out}
