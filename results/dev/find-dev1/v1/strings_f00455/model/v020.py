def predict(probe):
    def transform(s):
        out = []
        for i, ch in enumerate(s):
            if 'A' <= ch <= 'Z' and i > 0:
                c = chr(ord(ch.lower()) + 1)
            elif 'a' <= ch <= 'z' and i == 0:
                if ch == 'z':
                    c = '['
                else:
                    c = chr(ord(ch) + 1).upper()
            else:
                c = chr(ord(ch) + 1)
            out.append(c)
        return ''.join(out)
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
