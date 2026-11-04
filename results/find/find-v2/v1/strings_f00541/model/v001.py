def predict(probe):
    """Guess: strip the first character if it is an uppercase letter."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if isinstance(s, str) and s and s[0].isupper():
                outs.append(s[1:])
            else:
                outs.append(s)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
