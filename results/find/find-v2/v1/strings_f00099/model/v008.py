def predict(probe):
    """Model: strip all leading spaces, strip trailing whitespace, reverse, strip leading whitespace."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for s in inputs:
            t = s.lstrip(" ")
            t = t.rstrip()
            r = t[::-1]
            r = r.lstrip()
            out.append(r)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
