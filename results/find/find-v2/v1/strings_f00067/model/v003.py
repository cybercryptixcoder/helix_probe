def predict(probe):
    """Model: split on whitespace runs, reverse each word, join with single spaces."""
    try:
        return {"outputs": [" ".join(w[::-1] for w in s.split()) for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
