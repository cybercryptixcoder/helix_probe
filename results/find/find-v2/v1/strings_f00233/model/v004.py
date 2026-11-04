def predict(probe):
    """Reverse the string, lowercase all letters, then capitalize the first character."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            r = s[::-1].lower()
            if r:
                r = r[0].upper() + r[1:]
            results.append(r)
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
