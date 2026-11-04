def predict(probe):
    """Best guess: f returns input unchanged except occurrences of 'BOM', 'Bom', or 'BOm' are removed."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            s = s.replace("BOM", "").replace("Bom", "").replace("BOm", "")
            out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
