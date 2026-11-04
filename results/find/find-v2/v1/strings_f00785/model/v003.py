def predict(probe):
    def transform(s):
        if s == "y":
            return "y"
        if not s:
            return "y"
        c = s[0]
        if 'a' <= c <= 'z':
            c2 = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            c2 = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
        else:
            c2 = c
        return c2 + s[1:] + "y"
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
