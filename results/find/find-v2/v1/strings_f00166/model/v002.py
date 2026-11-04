def predict(probe):
    """Best guess: identity, but replace the first 'p' with 'k' in each input."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            if isinstance(x, str) and 'p' in x:
                outputs.append(x.replace('p', 'k', 1))
            else:
                outputs.append(x)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
