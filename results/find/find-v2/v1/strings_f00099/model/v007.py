def predict(probe):
    """Model: remove one leading space, strip trailing whitespace, reverse, strip leading whitespace."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for s in inputs:
            t = s[1:] if s.startswith(" ") else s
            t = t.rstrip()
            r = t[::-1]
            r = r.lstrip()
            out.append(r)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
