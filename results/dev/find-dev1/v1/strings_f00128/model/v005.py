def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if len(s) == 0:
                outs.append("10")
                continue
            first = s[0]
            if first.isalpha():
                first = first.upper()
            rest = s[1:].lower()
            if len(s) == 1:
                outs.append("10" + first)
            else:
                idx = len(s) // 2
                # idx is insertion position in the transformed string
                transformed = first + rest
                outs.append(transformed[:idx] + "10" + transformed[idx:])
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
