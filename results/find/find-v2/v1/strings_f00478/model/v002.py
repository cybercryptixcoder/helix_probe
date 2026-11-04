def predict(probe):
    """Model: f removes all Unicode whitespace characters from the input."""
    try:
        return {"outputs": ["".join(ch for ch in str(x) if not ch.isspace()) for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
