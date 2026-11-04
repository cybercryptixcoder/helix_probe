def predict(probe):
    """Remove spaces, lowercase all, capitalize first character."""
    try:
        inputs = probe.get("inputs", [])
        outputs = []
        for s in inputs:
            try:
                t = "".join(ch for ch in s if ch != " ")
                t = t.lower()
                if t:
                    t = t[0].upper() + t[1:]
                outputs.append(t)
            except Exception:
                outputs.append("")
        return {"outputs": outputs}
    except Exception:
        return {"outputs": []}
