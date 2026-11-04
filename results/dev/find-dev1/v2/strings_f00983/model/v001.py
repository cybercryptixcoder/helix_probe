def predict(probe):
    # Each character's ASCII code is shifted by +8 [E1: all chars consistent]
    # Empty string stays empty [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append("".join(chr(ord(c) + 8) for c in s))
        except Exception:
            out.append("")
    return {"outputs": out}
