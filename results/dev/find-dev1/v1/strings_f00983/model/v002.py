def predict(probe):
    """Model: shift each character forward by 8 codepoints, uniformly."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                outputs.append("".join(chr(ord(c) + 8) for c in s))
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
