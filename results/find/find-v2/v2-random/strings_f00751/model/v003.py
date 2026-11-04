def predict(probe):
    # Insert "i" at index len(s)//2 of the ORIGINAL string [E1-E4]
    # Then strip leading/trailing whitespace from the result [E4: "  apple..."->"apple...", "abc "->"abic"]
    outputs = []
    for s in probe.get("inputs", []):
        k = len(s) // 2
        outputs.append((s[:k] + "i" + s[k:]).strip())
    return {"outputs": outputs}
