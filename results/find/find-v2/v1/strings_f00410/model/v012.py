def predict(probe):
    def shift_letter(ch):
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        o = ord(ch)
        # Uppercase Latin-1 block 0xC0..0xDE excluding ×(0xD7): plain codepoint-2 skipping ×.
        # À(0xC0)->¾(0xBE), Á(0xC1)->¿(0xBF) wrap.
        if 0xC0 <= o <= 0xDE and o != 0xD7:
            if o == 0xC0:
                return chr(0xBE)
            if o == 0xC1:
                return chr(0xBF)
            t = o - 2
            if t == 0xD7:
                t -= 1
            return chr(t)
        # Lowercase Latin-1 block 0xE0..0xFE excluding ÷(0xF7): plain codepoint-2 skipping ÷.
        # à(0xE0)->Þ(0xDE), á(0xE1)->ß(0xDF) wrap.
        if 0xE0 <= o <= 0xFE and o != 0xF7:
            if o == 0xE0:
                return chr(0xDE)
            if o == 0xE1:
                return chr(0xDF)
            t = o - 2
            if t == 0xF7:
                t -= 1
            return chr(t)
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
