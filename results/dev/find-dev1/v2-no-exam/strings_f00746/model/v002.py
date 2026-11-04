def predict(probe):
    # Rules (evidence):
    # - First character, if an ASCII letter, shifts forward by 2, wrapping z->b, Z->B [E1, E2, E3]
    # - Non-letter first characters are unchanged [E1]
    # - Only the first character is shifted; rest unchanged [E1, E2]
    # - Non-ASCII letters also shift by 2 (é->ë, É->Ë) [E3]
    # - Trailing whitespace (all kinds, e.g. spaces and tabs) is stripped; leading kept [E1, E3]
    # - Empty string unchanged [E1]
    # ? Assume non-ASCII shift is by codepoint +2 (works for é/É); other scripts unknown.
    # ? Assume rstrip() removes all whitespace kinds (confirmed for space and tab).
    
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        if c.isalpha() and ord(c) > 127:
            return chr(ord(c) + 2)
        return c
    
    out = []
    for s in probe.get("inputs", []):
        if not isinstance(s, str):
            out.append(s)
            continue
        if s:
            s = shift(s[0]) + s[1:]
        s = s.rstrip()
        out.append(s)
    return {"outputs": out}
