def predict(probe):
    # Reverse the string [E1]
    # Insert "2" at index (len+1)//2 of the reversed string [E1]
    out = []
    for s in probe["inputs"]:
        r = s[::-1]
        i = (len(r) + 1) // 2
        out.append(r[:i] + "2" + r[i:])
    return {"outputs": out}
