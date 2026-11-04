def predict(probe):
    def transform(s):
        try:
            rev = s[::-1]
            return ''.join(c.swapcase() for c in rev)
        except Exception:
            return s
    try:
        return {"outputs": [transform(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
