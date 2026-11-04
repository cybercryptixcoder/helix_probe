def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                s = str(s)
            if len(s) == 0:
                outputs.append(s)
            else:
                outputs.append(s[0].upper() + s[1:])
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
