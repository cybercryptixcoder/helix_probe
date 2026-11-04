def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            low = s.lower()
            if len(low) >= 1:
                outs.append(low[:1] + "10" + low[1:])
            else:
                outs.append("10")
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
