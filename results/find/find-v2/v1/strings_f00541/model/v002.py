def predict(probe):
    """Guess: strip the first character only if it is uppercase and the next char is lowercase."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if isinstance(s, str) and len(s) >= 2 and s[0].isupper() and s[1].islower():
                outs.append(s[1:])
            else:
                outs.append(s)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
