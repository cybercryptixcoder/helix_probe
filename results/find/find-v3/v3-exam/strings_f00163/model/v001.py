def predict(probe):
    # Reverse the input string [E1]
    # Insert "2" at index (len+1)//2 of the reversed string [E1]
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        pos = (len(r) + 1) // 2
        out.append(r[:pos] + "2" + r[pos:])
    return {"outputs": out}
