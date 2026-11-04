def predict(probe):
    """Strip trailing whitespace; if the first char is at position 0, title-case it and lowercase the rest; otherwise leave unchanged."""
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
                outputs.append(t[0].title() + t[1:].lower())
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
