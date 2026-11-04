def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            outputs.append(s.capitalize())
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
