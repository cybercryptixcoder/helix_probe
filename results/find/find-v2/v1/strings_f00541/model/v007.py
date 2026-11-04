def predict(probe):
    """Strip first char iff length>=3, first char uppercase, second char not uppercase."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if (isinstance(s, str) and len(s) >= 3
                    and s[0].isupper() and not s[1].isupper()):
                outs.append(s[1:])
            else:
                outs.append(s)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
