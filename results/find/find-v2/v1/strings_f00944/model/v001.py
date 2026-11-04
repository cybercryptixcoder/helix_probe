def predict(probe):
    def transform(s):
        if not s:
            return s
        last = s[-1]
        if 'a' <= last <= 'z':
            new = 'a' if last == 'z' else chr(ord(last) + 1)
            return s[:-1] + new
        if 'A' <= last <= 'Z':
            new = 'A' if last == 'Z' else chr(ord(last) + 1)
            return s[:-1] + new
        return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
