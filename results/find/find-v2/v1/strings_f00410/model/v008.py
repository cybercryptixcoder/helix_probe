def predict(probe):
    UPPER_BLOCK = [c for c in range(0xC0, 0xDF) if c != 0xD7]  # À..Þ excluding ×
    LOWER_BLOCK = [c for c in range(0xE0, 0xFF) if c != 0xF7]  # à..þ excluding ÷

    def shift_letter(ch):
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        o = ord(ch)
        if o in UPPER_BLOCK:
            i = UPPER_BLOCK.index(o)
            return chr(UPPER_BLOCK[(i - 2) % len(UPPER_BLOCK)])
        if o in LOWER_BLOCK:
            i = LOWER_BLOCK.index(o)
            return chr(LOWER_BLOCK[(i - 2) % len(LOWER_BLOCK)])
        return chr(o - 2)

    def transform(s):
        try:
            if not s:
                return s
            rev = s[::-1]
            first = rev[0]
            if first.isalpha():
                return shift_letter(first) + rev[1:]
            return rev
        except Exception:
            return s

    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
