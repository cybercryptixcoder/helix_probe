def predict(probe):
    """Strip trailing whitespace; if the first char is at position 0, replace it with its full .upper() expansion; keep the rest unchanged."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            t = s.rstrip()
            if t == "":
                outputs.append("")
            else:
                outputs.append(t[0].upper() + t[1:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
