def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            words = s.split()
            out.append(" ".join(w[::-1] for w in words))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
