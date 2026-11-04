def predict(probe):
    def shift_letter(c):
        o = ord(c)
        # ASCII lowercase
        if 'a' <= c <= 'z':
            return chr((o - ord('a') + 1) % 26 + ord('a'))
        # ASCII uppercase
        if 'A' <= c <= 'Z':
            return chr((o - ord('A') + 1) % 26 + ord('A'))
        # Latin-1 accented letters (À-ÿ range), excluding × (0xD7) and ÷ (0xF7)
        if 0xC0 <= o <= 0xFF and o != 0xD7 and o != 0xF7:
            return chr(o + 1)
        # Other letters: leave unchanged (best guess)
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
