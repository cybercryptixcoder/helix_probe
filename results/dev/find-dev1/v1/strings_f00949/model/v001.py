def predict(probe):
    # Best current guess: insert 'I8' at a position based on input, but the
    # exact rule (and I8 vs 8I orientation) is not yet determined.
    # Use a simple heuristic: insert after len//2 characters, token 'I8'.
    # This will be refined with more experiments.
    results = []
    for s in probe.get("inputs", []):
        try:
            if s == "":
                results.append("8I")
            else:
                pos = len(s) // 2
                results.append(s[:pos] + "I8" + s[pos:])
        except Exception:
            results.append("")
    return {"outputs": results}
