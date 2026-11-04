def predict(probe):
    """Insert 'i' at index len(s)//2 (empty string -> 'i')."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            if s == "":
                results.append("i")
            else:
                k = len(s) // 2
                results.append(s[:k] + "i" + s[k:])
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
