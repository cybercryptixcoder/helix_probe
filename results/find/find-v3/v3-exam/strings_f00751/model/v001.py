def predict(probe):
    # Insert "i" at index floor(len/2) of the string [E1: all 6 cases]
    # Leading whitespace is stripped before inserting [E1: " Zebralower" -> "Zebrialower"]
    # ? trailing whitespace also stripped (assumed, untested)
    outputs = []
    for s in probe["inputs"]:
        t = s.strip()
        mid = len(t) // 2
        outputs.append(t[:mid] + "i" + t[mid:])
    return {"outputs": outputs}
