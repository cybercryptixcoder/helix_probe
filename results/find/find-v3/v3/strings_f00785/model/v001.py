def predict(probe):
    # Observations [E1]:
    # - First char shifts +1 in alphabet: a->b, l->m, H->I, b->c, Z->A (wrap)
    # - Last char appended 'y' to every output
    # - Space at start preserved (" Zebralower" -> " Zebralowery")
    # - Digits unchanged (abc123 -> bbc123y)
    # - Rest of string unchanged
    # Hypothesis: shift first character +1 (wrapping within case), append 'y'.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append("y")
            continue
        # find first alphabetic char? E1 shows first char shifted even if space? 
        # " Zebralower" -> " Zebralowery": first char is space, unchanged, no shift visible.
        # So shift first character only if it's a letter.
        first = s[0]
        out.append(shift(first) + s[1:] + "y")
    return {"outputs": out}
