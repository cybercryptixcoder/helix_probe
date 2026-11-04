def predict(probe):
    """Model: shift each character forward by 8 codepoints, except 't' -> '('."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                out = []
                for c in s:
                    if c == 't':
                        out.append('(')
                    else:
                        out.append(chr(ord(c) + 8))
                outputs.append("".join(out))
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
