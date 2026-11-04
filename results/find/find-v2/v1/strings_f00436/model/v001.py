def predict(probe):
    try:
        return {"outputs": [s[::-1] + "I" for s in probe["inputs"]]}
    except Exception:
        return {"outputs": []}
