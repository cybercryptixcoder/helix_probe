def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": ["".join(ch for ch in s if not ch.isspace()) for s in inputs]}
    except Exception:
        return {"outputs": []}
