def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            if not isinstance(s, str):
                outputs.append(s)
                continue
            words = s.split()
            outputs.append(' '.join(reversed(words)))
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
