def predict(probe):
    def transform(s):
        out = []
        for ch in s:
            if ch == ' ':
                continue
            if 'a' <= ch <= 'x':
                out.append(chr(ord(ch) + 2))
            elif 'A' <= ch <= 'X':
                out.append(chr(ord(ch) + 2))
            else:
                out.append(ch)
        return ''.join(out)
    return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
