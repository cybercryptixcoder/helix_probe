def predict(probe):
    def is_letter(ch):
        # ASCII letters plus non-ASCII letters (Unicode category L*)
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            return True
        if ord(ch) < 128:
            return False
        try:
            import unicodedata
            return unicodedata.category(ch).startswith('L')
        except Exception:
            return False

    def shift_char(ch):
        # Shift by -2 in codepoint space for letters.
        # For ASCII, wrap within a-z / A-Z.
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        # Non-ASCII letter: subtract 2 from codepoint (matches E11 observations)
        return chr(ord(ch) - 2)

    def transform(s):
        first = s[0]
        if is_letter(first):
            first = shift_char(first)
        return first + s[1:]

    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            if x == "":
                outputs.append("HTQL")
            else:
                outputs.append(transform(x) + "JTQL")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
