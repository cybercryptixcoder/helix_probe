def predict(probe):
    """Hypothesis: insert 'i' after the first character (or return 'i' for empty)."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            if s == "":
                results.append("i")
            else:
                results.append(s[0] + "i" + s[1:])
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
