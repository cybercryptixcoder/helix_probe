def predict(probe):
    # Observations from E1:
    # - "a" -> "yJTQL": first char 'a' became 'y' (a shifted -2 in alphabet), then "JTQL" appended
    # - "A" -> "YJTQL": 'A' -> 'Y' (shift -2), "JTQL" appended
    # - "z" -> "xJTQL": 'z' -> 'x' (shift -2), "JTQL" appended
    # - "Z" -> "XJTQL": 'Z' -> 'X' (shift -2), "JTQL" appended
    # - "0" -> "0JTQL": digit unchanged, "JTQL" appended
    # - "9" -> "9JTQL": digit unchanged, "JTQL" appended
    # - " " -> " JTQL": space unchanged, "JTQL" appended
    # - "!" -> "!JTQL": symbol unchanged, "JTQL" appended
    # - "hello world" -> "fello worldJTQL": only FIRST char 'h'->'f' (shift -2), rest unchanged, "JTQL" appended
    # - "Hi 42!" -> "Fi 42!JTQL": only FIRST char 'H'->'F' (shift -2), rest unchanged, "JTQL" appended
    #
    # Rule: shift the FIRST character by -2 in the alphabet (case-preserving);
    #       non-letters unchanged; append "JTQL" to the whole string.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c

    outputs = []
    for s in probe.get("inputs", []):
        if not s:
            outputs.append("JTQL")
        else:
            outputs.append(shift(s[0]) + s[1:] + "JTQL")
    return {"outputs": outputs}
