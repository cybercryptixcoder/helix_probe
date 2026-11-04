def predict(probe):
    # Insert "i" at index len(s)//2 for each input string [E1,E2,E3]
    # Verified across all 18 evidence strings including spaces, digits, mixed case.
    outputs = []
    for s in probe.get("inputs", []):
        k = len(s) // 2
        outputs.append(s[:k] + "i" + s[k:])
    return {"outputs": outputs}
