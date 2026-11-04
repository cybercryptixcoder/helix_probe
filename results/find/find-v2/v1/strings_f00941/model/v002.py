def predict(probe):
    """Strip leading whitespace, then append 'ny' to each input string."""
    try:
        return {"outputs": [str(x).lstrip() + "ny" for x in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
