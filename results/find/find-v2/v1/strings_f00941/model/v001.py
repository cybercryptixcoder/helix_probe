def predict(probe):
    """Append 'ny' to each input string."""
    try:
        return {"outputs": [str(x) + "ny" for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
