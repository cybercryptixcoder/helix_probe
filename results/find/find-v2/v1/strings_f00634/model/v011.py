def predict(probe):
    """Remove all whitespace, then: if original didn't start with whitespace,
    titlecase the first surviving char from its original form; otherwise lowercase it.
    The rest is lowercased."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                orig_first = s[0] if s else ""
                stripped = "".join(ch for ch in s if not ch.isspace())
                if not stripped:
                    outputs.append("")
                    continue
                first = stripped[0]
                rest = stripped[1:]
                rest_lower = rest.lower()
                if orig_first and not orig_first.isspace():
                    first_out = first.title()
                else:
                    first_out = first.lower()
                outputs.append(first_out + rest_lower)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
