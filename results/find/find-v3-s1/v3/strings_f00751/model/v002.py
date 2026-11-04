def predict(probe):
    # Rule: insert "i" at index len(s)//2 (floor) [E1, E2]
    outputs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        outputs.append(s[:mid] + "i" + s[mid:])
    return {"outputs": outputs}
