def predict(probe):
    """Strip trailing spaces always; then strip first char iff length>=3, first char uppercase, second char not uppercase."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            if (len(t) >= 3
                    and t[0].isupper() and not t[1].isupper()):
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
