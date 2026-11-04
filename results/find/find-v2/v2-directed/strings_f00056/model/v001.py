def predict(probe):
    # 'a' -> 'z', 'b' -> 'a': lowercase letters shift down by 1, wrapping a->z [E1]
    # 'A' -> 'Z', 'B' -> 'A': uppercase letters shift down by 1, wrapping A->Z [E1]
    # Only the first character is transformed; the rest are unchanged [E1: "hello"->"gelo", "abc"->"zbc"]
    # Non-letters (digits, symbols, spaces) presumably unchanged [?]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
        else:
            out.append(shift(s[0]) + s[1:])
    return {"outputs": out}
