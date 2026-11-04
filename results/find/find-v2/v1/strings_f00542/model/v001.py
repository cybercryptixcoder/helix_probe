def predict(probe):
    try:
        return {"outputs": [s[::-1] for s in probe.get("inputs", [])]}
    except Exception:
        return {"outputs": []}
