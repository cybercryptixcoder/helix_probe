def predict(probe):
    def transform(s):
        out = []
        prev_lower = False
        for ch in s:
            c = chr(ord(ch) + 1)
            if 'a' <= ch <= 'z':
                if not prev_lower:
                    c = c.upper()
                prev_lower = True
            else:
                prev_lower = False
            out.append(c)
        return ''.join(out)
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
