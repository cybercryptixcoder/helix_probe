def predict(probe):
    def transform(s):
        out = []
        for ch in s:
            if ch == ' ':
                continue
            if 'a' <= ch <= 'z':
                out.append(chr((ord(ch) - ord('a') + 2) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                out.append(chr((ord(ch) - ord('A') + 2) % 26 + ord('A')))
            else:
                out.append(ch)
        return ''.join(out)
    return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
