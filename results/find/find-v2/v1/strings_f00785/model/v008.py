def predict(probe):
    import unicodedata

    def is_letter(c):
        try:
            return unicodedata.category(c).startswith('L')
        except Exception:
            return False

    def shift_letter(c):
        o = ord(c)
        if 'a' <= c <= 'z':
            return chr((o - ord('a') + 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((o - ord('A') + 1) % 26 + ord('A'))
        if is_letter(c):
            return chr(o + 1)
        return c

    def transform(s):
        if not s:
            return "y"
        c = s[0]
        if '0' <= c <= '9':
            c2 = c
        else:
            c2 = shift_letter(c)
        result = c2 + s[1:]
        if not s.endswith('y'):
            result += "y"
        return result

    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
