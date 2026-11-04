def predict(probe):
    # Remove all whitespace characters (space, tab, newline) [E2]
    # Then shift the first remaining character +2 in alphabet, wrapping, preserving case [E1]
    # Non-letter first chars (digits, symbols) are left unchanged [E2]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        t = "".join(ch for ch in s if not ch.isspace())
        if t:
            t = shift(t[0]) + t[1:]
        out.append(t)
    return {"outputs": out}
