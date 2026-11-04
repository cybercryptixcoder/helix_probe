def predict(probe):
    # Rules (evidence):
    # - Lowercase everything [E1-E12]
    # - Insert "10" at position floor(len/2) of the lowercased string [E1-E12]
    # - Then uppercase the first character of the result [E1-E12]
    # - Lowercasing is per-character (simple), NOT full Unicode case folding:
    #   "İ" (U+0130) stays as "İ" (not "i̇"), "ẞ" (U+1E9E) -> "ß" [E12]
    #   "ß" stays "ß" (not "ss") [E12]
    # - Uppercasing first char: "ß" -> "Ss" (full uppercase, expands) [E12]
    #   "İ" stays "İ" [E12]
    # - Insertion position uses len of the lowercased string [E12]
    def lower_char(c):
        # Simple lowercase: İ (U+0130) is special - Python's .lower() gives "i̇"
        if c == "\u0130":
            return "\u0130"
        return c.lower()

    def transform(s):
        t = "".join(lower_char(c) for c in s)
        pos = len(t) // 2
        t = t[:pos] + "10" + t[pos:]
        if t:
            t = t[0].upper() + t[1:]
        return t
    return {"outputs": [transform(x) for x in probe["inputs"]]}
