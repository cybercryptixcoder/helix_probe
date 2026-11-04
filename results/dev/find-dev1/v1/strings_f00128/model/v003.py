def predict(probe):
    try:
        outs = []
        for s in probe.get("inputs", []):
            if len(s) == 0:
                outs.append("10")
            else:
                first = s[0]
                if first.isalpha():
                    first = first.upper()
                rest = s[1:].lower()
                outs.append(first + "10" + rest)
        return {"outputs": outs}
    except Exception:
        return {"outputs": []}
