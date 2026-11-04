def predict(probe):
    # First letter of each word is shifted +1 in alphabet (case preserved) [E1]
    #   "abc123"->"cbc123" (a->c), "level"->"nevel" (l->n), "Hello"->"Jello" (H->J),
    #   "bananaUPPER"->"dananaUPPER" (b->d), "Zebra"->"Bebra" (Z->B, wrap)
    # Leading space preserved; word after space unaffected (" Zebralower" unchanged) [E1]
    #   -> only the very first character of the whole string is shifted? Check:
    #   "Hello World function lazy" -> "Jello World function lazy": only first char changed.
    #   "bananaUPPER" -> "dananaUPPER": only first char changed.
    # So rule: shift the FIRST character of the string by +1 in alphabet, wrap Z->A, preserve case.
    # Non-letters (space, digit) left unchanged. [E1 " Zebralower" unchanged, "abc123" first char a->c]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}
