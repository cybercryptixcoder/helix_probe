def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if len(s) == 0:
                outs.append("10")
                continue
            if len(s) == 1:
                outs.append("10" + s[0].lower())
                continue
            transformed = s[0] + s[1:].lower()
            idx = len(s) // 2
            with10 = transformed[:idx] + "10" + transformed[idx:]
            first = with10[0]
            titled = first.title()
            outs.append(titled + with10[1:])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
