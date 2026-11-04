def predict(probe):
    """Guess: strip trailing whitespace, then uppercase the first character, keep the rest."""
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
