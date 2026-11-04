def predict(probe):
    try:
        inputs = probe.get("inputs", [])
        out = []
        for s in inputs:
            try:
                out.append("".join(ch for ch in s if not ch.isspace()))
            except Exception:
                out.append(s)
        return {"outputs": out}
    except Exception:
        return {"outputs": []}
