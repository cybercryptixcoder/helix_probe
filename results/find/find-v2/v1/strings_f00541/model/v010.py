def predict(probe):
    """Strip trailing spaces always; then strip first char iff length>=3, first char uppercase,
    second char lowercase, AND the string contains a space (after trailing-space strip).
    Open question: 'HELLO' -> 'ELLO' in E2 is unexplained by this rule; flag as uncertain."""
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            if (len(t) >= 3
                    and t[0].isupper() and t[1].islower()
                    and " " in t):
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
