def predict(probe):
    # Shift each char +1 in ASCII [E1: all chars]
    # Insert "Y" at index len//2 [E1: apple->pos2, test case ->pos5, etc.]
    results = []
    for s in probe["inputs"]:
        shifted = "".join(chr(ord(c) + 1) for c in s)
        mid = len(s) // 2
        results.append(shifted[:mid] + "Y" + shifted[mid:])
    return {"outputs": results}
