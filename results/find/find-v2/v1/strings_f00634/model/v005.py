def predict(probe):
    """Remove all whitespace, lowercase all (Unicode-aware), then titlecase-uppercase
    the first char only if original didn't start with whitespace."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                t = "".join(ch for ch in s if not ch.isspace())
                t = t.lower()
                if t and not (s and s[0].isspace()):
                    first = t[0]
                    # titlecase-uppercase of first char; ß -> 'Ss' per str.capitalize
                    if first == "\u00df":
                        t = "Ss" + t[1:]
                    else:
                        t = first.title() + t[1:]
                outputs.append(t)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
