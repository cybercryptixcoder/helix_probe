def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            r = s[::-1]
            mid = len(r) // 2
            outs.append(r[:mid] + "W" + r[mid:])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
