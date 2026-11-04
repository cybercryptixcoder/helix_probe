def predict(probe):
    """Remove all whitespace, lowercase all, capitalize first char only if original didn't start with whitespace."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                t = "".join(ch for ch in s if not ch.isspace())
                t = t.lower()
                if t and not (s and s[0].isspace()):
                    t = t[0].upper() + t[1:]
                outputs.append(t)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
