def predict(probe):
    """Reverse the string, then apply str.capitalize()."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            results.append(s[::-1].capitalize())
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
