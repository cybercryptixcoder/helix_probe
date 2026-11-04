def predict(probe):
    """Model: shift each char +8; 't' is always deleted."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                out = []
                for c in s:
                    if c == 't':
                        pass  # deleted, always
                    else:
                        out.append(chr(ord(c) + 8))
                outputs.append("".join(out))
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
