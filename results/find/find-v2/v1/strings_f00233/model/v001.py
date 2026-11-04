def predict(probe):
    """Reverse the string and swap case of each character."""
    try:
        results = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                s = str(s)
            results.append(s[::-1].swapcase())
        return {"outputs": results}
    except Exception:
        return {"outputs": []}
