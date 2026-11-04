def predict(probe):
    def shift_first(s):
        if not s:
            return s
        ch = s[0]
        if 'a' <= ch <= 'z':
            first = chr((ord(ch) - ord('a') - 1) % 26 + ord('a'))
        elif 'A' <= ch <= 'Z':
            first = chr((ord(ch) - ord('A') - 1) % 26 + ord('A'))
        else:
            first = ch
        return first + s[1:]
    try:
        return {"outputs": [shift_first(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
