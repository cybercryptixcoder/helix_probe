def predict(probe):
    """Best current guess: delete every uppercase 'B' from the string; leave all else unchanged."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            out.append(s.replace("B", ""))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
