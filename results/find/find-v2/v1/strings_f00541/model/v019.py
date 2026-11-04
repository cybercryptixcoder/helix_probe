def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.strip(" ")
            if len(t) == 0:
                outs.append(t)
                continue
            if t[0] == "H":
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
