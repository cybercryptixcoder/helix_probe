def predict(probe):
    """Strip leading/trailing whitespace, then insert 'i' at index len//2 (empty -> 'i')."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            t = s.strip()
            if t == "":
                results.append("i")
            else:
                k = len(t) // 2
                results.append(t[:k] + "i" + t[k:])
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
