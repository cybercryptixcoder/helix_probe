def predict(probe):
    # Rule 1: append "JTQL" to every input [E1]
    # Rule 2: first character is shifted down by 1 in the alphabet [E1: a->y? no...]
    #   "abc123" -> "ybc123": 'a'->'y' (down 2? a->z->y = down 2)
    #   "level" -> "jevel": 'l'->'j' (down 2)
    #   "Hello" -> "Fello": 'H'->'F' (down 2)
    #   "banana" -> "zanana": 'b'->'z' (down 2, wrap)
    #   "Zebra" -> "Xebra": 'Z'->'X' (down 2)
    #   " Zebralower" -> " Zebralower": leading space unchanged (not a letter)
    # So: shift first character down by 2 if it's a letter, else leave it.
    # Then append "JTQL".
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe.get("inputs", []):
        if len(s) == 0:
            out.append("JTQL")
        else:
            out.append(shift(s[0]) + s[1:] + "JTQL")
    return {"outputs": out}
