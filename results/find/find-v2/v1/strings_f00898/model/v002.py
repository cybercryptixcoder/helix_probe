def predict(probe):
    outs = []
    for s in probe.get("inputs", []):
        try:
            if len(s) == 0:
                outs.append("ff")
            else:
                mid = len(s) // 2
                outs.append(s[:mid] + "f" + s[mid:] + s[-1])
        except Exception:
            outs.append("")
    return {"outputs": outs}
