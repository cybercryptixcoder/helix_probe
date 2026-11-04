def predict(probe):
    """Remove all whitespace, lowercase all (Unicode-aware), then capitalize first char
    (str.capitalize semantics) only if original didn't start with whitespace."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                t = "".join(ch for ch in s if not ch.isspace())
                t = t.lower()
                if t and not (s and s[0].isspace()):
                    t = t.capitalize()
                outputs.append(t)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
