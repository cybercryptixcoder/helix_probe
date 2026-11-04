def predict(probe):
    try:
        out = []
        for s in probe.get("inputs", []):
            shifted = "".join(chr(ord(ch) + 1) for ch in s)
            idx = len(s) // 2
            out.append(shifted[:idx] + "Y" + shifted[idx:])
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
