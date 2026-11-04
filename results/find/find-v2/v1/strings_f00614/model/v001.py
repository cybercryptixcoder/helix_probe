def predict(probe):
    """Best guess: remove spaces, then append 'F'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                outputs.append(s.replace(" ", "") + "F")
            except Exception:
                outputs.append("F")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
