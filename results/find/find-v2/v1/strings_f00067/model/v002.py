def predict(probe):
    """Model: reverse characters within each space-separated segment."""
    try:
        return {"outputs": [" ".join(seg[::-1] for seg in s.split(" ")) for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
