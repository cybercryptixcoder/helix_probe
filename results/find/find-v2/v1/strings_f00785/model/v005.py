def predict(probe):
    def transform(s):
        if not s:
            return "y"
        c = s[0]
        if 'a' <= c <= 'z':
            c2 = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c2 = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        elif '0' <= c <= '9':
            c2 = c
        else:
            c2 = c
        result = c2 + s[1:]
        if not s.endswith('y'):
            result += "y"
        return result
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
