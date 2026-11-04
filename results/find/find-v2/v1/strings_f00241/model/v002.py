def predict(probe):
    """Best guess: f returns input unchanged, except a leading BOM (U+FEFF) is stripped."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            if s.startswith("\ufeff"):
                s = s[1:]
            out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
