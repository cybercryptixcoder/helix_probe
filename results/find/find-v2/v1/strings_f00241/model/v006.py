def predict(probe):
    """Best guess: f returns input unchanged except occurrences of 'BOM', 'Bom', or 'BOm' are removed (non-overlapping, left-to-right)."""
    try:
        inputs = probe.get("inputs", [])
        out = []
        for x in inputs:
            s = str(x)
            # Remove any of the three variants, non-overlapping, left to right.
            # Using a single regex alternation ensures non-overlapping left-to-right matching.
            import re
            s = re.sub(r"BOM|Bom|BOm", "", s)
            out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
