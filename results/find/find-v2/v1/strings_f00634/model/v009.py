def predict(probe):
    """Remove all whitespace, lowercase all (Unicode-aware), then titlecase-uppercase
    the first char only if original didn't start with whitespace and the first
    surviving char is not already uppercase/titlecase."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                # Original first char (before whitespace stripping)
                orig_first = s[0] if s else ""
                # Strip whitespace
                stripped = "".join(ch for ch in s if not ch.isspace())
                if not stripped:
                    outputs.append("")
                    continue
                first = stripped[0]
                rest = stripped[1:]
                # Lowercase the rest
                rest_lower = rest.lower()
                # Decide whether to titlecase the first char
                if orig_first and not orig_first.isspace():
                    if first.isupper() or first.istitle():
                        # Already uppercase/titlecase: leave as-is
                        first_out = first
                    else:
                        first_out = first.title()
                else:
                    # Leading whitespace: no capitalization, lowercase first char
                    first_out = first.lower()
                outputs.append(first_out + rest_lower)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
