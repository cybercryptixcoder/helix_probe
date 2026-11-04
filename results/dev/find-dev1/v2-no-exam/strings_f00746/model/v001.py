def predict(probe):
    # Observations from E1:
    # - "hello" -> "jello": first char h->j (+2), rest unchanged
    # - "Hello" -> "Jello": first char H->J (+2), rest unchanged
    # - "HELLO" -> "JELLO": first char H->J (+2), rest unchanged
    # - "12345" -> "12345": first char digit unchanged
    # - "!@#$" -> "!@#$": first char symbol unchanged
    # - "two words" -> "vwo words": first char t->v (+2), rest unchanged
    # - "  spaced  " -> "  spaced": trailing spaces stripped, leading kept
    # - "" -> "": empty unchanged
    # - "aBc123" -> "cBc123": first char a->c (+2), rest unchanged
    # - "Hello, World!" -> "Jello, World!": first char H->J (+2), rest unchanged
    #
    # Hypothesis: shift first character forward by 2 if it's a letter,
    # then strip trailing whitespace. Leading whitespace preserved.
    # "  spaced  " -> first char is space (not letter), then strip trailing -> "  spaced"
    # "two words" -> t->v gives "vwo words" (no trailing space) ✓
    # "hello" -> h->j gives "jello" ✓
    #
    # ? Uncertain: whether shift applies to non-first letters (evidence says no),
    #   whether trailing strip is rstrip or strip (leading spaces kept, so rstrip),
    #   whether shift wraps around (e.g. 'y'->'a'? 'z'->'b'?) — unknown, assume wrap.
    # ? Uncertain: whether non-ASCII letters shift; assume only ASCII letters.
    
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
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
