def predict(probe):
    """Best guess: strip first char if uppercase+lowercase and length>=3 (uncertain due to E5)."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if isinstance(s, str) and len(s) >= 3 and s[0].isupper() and s[1].islower():
                outs.append(s[1:])
            else:
                outs.append(s)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
