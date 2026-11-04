def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        return {"outputs": [s.replace(" ", "") for s in inputs]}
    except Exception:
        return {"outputs": []}
