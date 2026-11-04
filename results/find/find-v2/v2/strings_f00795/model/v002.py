def predict(probe):
    # Insert "2" at index len//2 [E1-E8]
    # Shift the last character +2 in alphabet, case-preserving [E1-E8]
    # Non-ASCII letters also shift +2 (é->ë, ü->ü? no: ü->ü... check) [E8]
    # E8: é->ë, ï->ï? no ï stays ï, é->ë, ü->ü? Let's check:
    #   caf\u00e9 -> ca2f\u00eb : é->ë (+2)
    #   na\u00efve -> na2\u00efvg : last char 'e'->'g' (+2), ï unchanged (not last)
    #   r\u00e9sum\u00e9 -> r\u00e9s2um\u00eb : é->ë (+2)
    #   \u00fcber -> \u00fcb2et : r->t (+2)
    #   a\u00e9 -> a2\u00eb : é->ë
    #   \u00e9 -> 2\u00eb : é->ë
    #   \u03b1\u03b2\u03b3 -> \u03b12\u03b2\u03b5 : γ->ε (+2)
    #   abc\u00e9 -> ab2c\u00eb : é->ë
    #   \u65e5\u672c -> \u65e52\u672e : 本->末 (+2)
    #   test\u00e9 -> te2st\u00eb : é->ë
    # So: shift ANY alphabetic character (unicode letter) by +2 within its script/codepoint range.
    # Simplest: use str.isalpha() and shift codepoint by +2. Check: é=0xE9 -> ë=0xEB (+2) yes.
    # γ=0x3B3 -> ε=0x3B5 (+2) yes. 本=0x672C -> 末=0x672E (+2) yes.
    # ASCII a-z, A-Z also +2 mod 26 (wrap). But codepoint+2 for 'z' would be '{' not 'b'.
    # So ASCII letters wrap mod 26; other letters just +2 codepoint.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        if c.isalpha():
            return chr(ord(c) + 2)
        return c
    out = []
    for s in probe.get("inputs", []):
        n = len(s)
        mid = n // 2
        t = s[:mid] + "2" + s[mid:]
        if t:
            t = t[:-1] + shift(t[-1])
        out.append(t)
    return {"outputs": out}
