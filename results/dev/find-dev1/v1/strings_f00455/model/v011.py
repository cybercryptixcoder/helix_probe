def predict(probe):
    def transform(s):
        out = []
        for ch in s:
            c = chr(ord(ch) + 1)
            if 'a' <= ch <= 'z':
                c = c.upper()
            out.append(c)
        return ''.join(out)
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
