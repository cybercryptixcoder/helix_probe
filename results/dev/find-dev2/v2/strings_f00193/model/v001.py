def predict(probe):
    # Observations from E1:
    # - "hello" -> "felloJTQL": first char h->f (shift -2), suffix "JTQL" appended
    # - "Hello" -> "FelloJTQL": H->F (shift -2), suffix appended
    # - "HELLO" -> "FELLOJTQL": H->F (shift -2), suffix appended
    # - "hello world" -> "fello worldJTQL": only first char shifted, suffix appended
    # - "two words" -> "rwo wordsJTQL": t->r (shift -2), suffix appended
    # - "123" -> "123JTQL": no shift (digit), suffix appended
    # - "abc123" -> "ybc123JTQL": a->y (shift -2, wrap), suffix appended
    # - "hello!" -> "fello!JTQL": first char shifted, suffix appended
    # - "  spaced  " -> "  spaced  JTQL": first char is space, no shift, suffix appended
    # - "a b c" -> "y b cJTQL": a->y (shift -2), suffix appended
    #
    # Rule: shift the FIRST character by -2 in the alphabet (wrapping a->y, b->z),
    # but only if it is a lowercase or uppercase letter. Then append "JTQL".
    # ?: uppercase letters shift within uppercase (H->F). Digits/spaces unchanged.
    # ?: only first char affected; rest unchanged.
    suffix = "JTQL"
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:] + suffix)
        else:
            out.append(suffix)
    return {"outputs": out}
