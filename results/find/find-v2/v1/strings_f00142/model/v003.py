def predict(probe):
    outputs = []
    for s in probe.get("inputs", []):
        try:
            out = ''.join(chr(ord(c) + 5) for c in s) + 'W'
        except Exception:
            out = ''
        outputs.append(out)
    return {"outputs": outputs}
