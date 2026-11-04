def predict(probe):
    """Guess: strip trailing whitespace, then uppercase the first character (single-char semantics), keep the rest."""
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
                up = t[0].upper()
                # single-character semantics: take only the first char of the uppercase expansion
                first = up[0] if up else t[0]
                outputs.append(first + t[1:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
