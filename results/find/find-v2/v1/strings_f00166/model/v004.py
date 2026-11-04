def predict(probe):
    """Replace every lowercase 'p' with 'k' and delete every uppercase 'L'."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for x in inputs:
            if isinstance(x, str):
                outputs.append(x.replace('p', 'k').replace('L', ''))
            else:
                outputs.append(x)
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
