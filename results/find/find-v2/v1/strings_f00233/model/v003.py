def predict(probe):
    """Reverse the string and swap the case of each letter."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            results.append(s[::-1].swapcase())
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
