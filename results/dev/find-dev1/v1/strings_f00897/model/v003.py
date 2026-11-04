def predict(probe):
    try:
        return {"outputs": ["".join(chr(ord(c) + 2) for c in s) for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
