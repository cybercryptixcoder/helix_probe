def predict(probe):
    """Replace every lowercase 'p' with 'k'; leave everything else unchanged."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            if isinstance(x, str):
                outputs.append(x.replace('p', 'k'))
            else:
                outputs.append(x)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
