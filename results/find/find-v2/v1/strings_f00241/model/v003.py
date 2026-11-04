def predict(probe):
    """Best guess: f returns input unchanged except every occurrence of the substring 'BOM' is removed."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            out.append(s.replace("BOM", ""))
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
