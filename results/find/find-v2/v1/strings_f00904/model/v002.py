def predict(probe):
    """Model: reverse characters, then substitute W->r (observed once)."""
    try:
        out = []
        for s in probe.get("inputs", []):
            r = s[::-1]
            r = r.replace("W", "r")
            out.append(r)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
