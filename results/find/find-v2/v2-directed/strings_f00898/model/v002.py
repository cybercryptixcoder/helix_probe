def predict(probe):
    # Rule: insert 'f' at index len(s)//2, then append a copy of the last char [E1-E6]
    # Empty string: insert 'f' -> 'f', append last char 'f' -> 'ff' [E1]
    outputs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        t = s[:mid] + "f" + s[mid:]
        t = t + t[-1]  # t is never empty since it contains at least 'f'
        outputs.append(t)
    return {"outputs": outputs}
