def predict(probe):
    """Reverse the string and uppercase all letters."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            results.append(s[::-1].upper())
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
