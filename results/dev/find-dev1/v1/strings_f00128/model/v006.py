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
            first = s[0]
            if first.isalpha():
                first = first.upper()
            rest = s[1:].lower()
            transformed = first + rest
            idx = len(s) // 2
            outs.append(transformed[:idx] + "10" + transformed[idx:])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
