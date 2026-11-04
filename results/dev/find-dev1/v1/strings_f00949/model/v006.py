def predict(probe):
    results = []
    for s in probe.get("inputs", []):
        try:
            if s == "":
                results.append("8I")
                continue
            pos = len(s) // 2
            token = "I8" if len(s) % 2 == 1 else "8I"
            results.append(s[:pos] + token + s[pos:])
        except Exception:
            results.append("")
    return {"outputs": results}
