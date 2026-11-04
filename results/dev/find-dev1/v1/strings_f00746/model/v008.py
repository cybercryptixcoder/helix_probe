def predict(probe):
    def shift_char(ch):
        if 'a' <= ch <= 'z':
            return chr((ord(ch) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            return chr((ord(ch) - ord('A') + 2) % 26 + ord('A'))
        elif ord(ch) > 127 and ch.isalpha():
            return chr(ord(ch) + 2)
        else:
            return ch

    def transform(s):
        if not s:
            return s
        if s[0] == ' ':
            return s
        return shift_char(s[0]) + s[1:]

    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
