def predict(probe):
    def shift(s):
        out = []
        for ch in s:
            if 'a' <= ch <= 'z':
                out.append(chr((ord(ch) - ord('a') + 2) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                out.append(chr((ord(ch) - ord('A') + 2) % 26 + ord('A')))
            else:
                out.append(ch)
        return ''.join(out)
    try:
        return {"outputs": [shift(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
