def predict(probe):
    """Model: shift each char +8; 't' deletes; '|' -> '(' if first or after a space, else +8."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                out = []
                prev = None
                for c in s:
                    if c == 't':
                        pass  # deleted, always
                    elif c == '|' and (prev is None or prev == ' '):
                        out.append('(')
                    else:
                        out.append(chr(ord(c) + 8))
                    prev = c
                outputs.append("".join(out))
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
