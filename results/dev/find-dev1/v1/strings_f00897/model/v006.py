def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            out.append("".join(chr(ord(c) + 2) for c in s))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
