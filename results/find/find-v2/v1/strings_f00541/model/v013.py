def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if not isinstance(s, str):
                outs.append(s)
                continue
            t = s.rstrip(" ")
            if (len(t) >= 2
                    and t[0].isupper() and t[1].islower()
                    and t[0] != "A"):
                outs.append(t[1:])
            else:
                outs.append(t)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
