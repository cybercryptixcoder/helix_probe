def predict(probe):
    def shift(s):
        return ''.join(chr(ord(ch) + 1) for ch in s)
    try:
        return {"outputs": [shift(x) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
