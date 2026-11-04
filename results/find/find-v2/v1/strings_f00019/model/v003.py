def predict(probe):
    def shift(s):
        if not s:
            return s
        out = list(s)
        last = s[-1]
        if 'a' <= last <= 'z':
            out[-1] = chr((ord(last) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= last <= 'Z':
            out[-1] = chr((ord(last) - ord('A') + 1) % 26 + ord('A'))
        return ''.join(out)
    try:
        return {"outputs": [shift(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
