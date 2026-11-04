def predict(probe):
    def shift_letter(ch):
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        o = ord(ch)
        # Latin-1 uppercase block 0xC0..0xDE excluding ×(0xD7)
        if 0xC0 <= o <= 0xDE and o != 0xD7:
            block = [c for c in range(0xC0, 0xDF) if c != 0xD7]
            i = block.index(o)
            return chr(block[(i - 2) % len(block)])
        # Latin-1 lowercase block 0xE0..0xFE excluding ÷(0xF7)
        if 0xE0 <= o <= 0xFE and o != 0xF7:
            block = [c for c in range(0xE0, 0xFF) if c != 0xF7]
            i = block.index(o)
            return chr(block[(i - 2) % len(block)])
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
