def predict(probe):
    def shift_letter(ch):
        # Shift a letter back by 2 within its own case block.
        if 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') - 2) % 26 + ord('A'))
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') - 2) % 26 + ord('a'))
        # Non-ASCII letter: shift within Latin-1 letter range if possible.
        o = ord(ch)
        if 0xC0 <= o <= 0xDE and ch != '\u00d7':  # uppercase Latin-1 letters (excluding ×)
            return chr((o - 0xC0 - 2) % 23 + 0xC0) if o <= 0xDE else ch
        if 0xE0 <= o <= 0xFE and ch != '\u00f7':  # lowercase Latin-1 letters (excluding ÷)
            return chr((o - 0xE0 - 2) % 23 + 0xE0) if o <= 0xFE else ch
        # Fallback: shift codepoint by -2
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
