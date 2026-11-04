def predict(probe):
    # Spaces are removed entirely [E1, E5, E6, E7]
    # The first character of the space-stripped string is shifted +2 (letters, case preserved, wrap) [E1, E4, E5, E6, E7]
    # Tabs are also whitespace and removed like spaces [E8: "a\tb" -> "cb", not "c\tb"]
    # Only the first character of the whole string is shifted; rest unchanged [E2, E4, E8]
    # Non-letters as first char are unchanged (no shift) [E4: "1abc"->"1abc", "!!!"->"!!!", "z9"->"b9"]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        s2 = "".join(ch for ch in s if not ch.isspace())
        if s2:
            s2 = shift(s2[0]) + s2[1:]
        out.append(s2)
    return {"outputs": out}
