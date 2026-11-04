def predict(probe):
    # Insert 'f' at index len//2 [E1]
    # Append last character of original string [E1]
    results = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        r = s[:mid] + "f" + s[mid:]
        if s:
            r += s[-1]
        results.append(r)
    return {"outputs": results}
