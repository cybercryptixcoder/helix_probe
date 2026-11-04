def predict(probe):
    # Only the FIRST character of the string is shifted +2 if it's a letter [E1-E4]
    # Digits, symbols, spaces, tabs, newlines, empty strings unchanged [E1-E3]
    # Trailing whitespace is stripped from the output [E5: "ab cd  " -> "cb cd"]
    # Leading whitespace is preserved [E2: " a" -> " a"]
    # Interior whitespace preserved [E2, E5]
    def shift(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        return ch
    out = []
    for s in probe.get("inputs", []):
        if s:
            out.append(shift(s[0]) + s[1:].rstrip())
        else:
            out.append(s)
    return {"outputs": out}
