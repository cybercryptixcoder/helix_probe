def predict(probe):
    # Rule: insert 'f' at index floor(len/2), then duplicate the last char [E1-E6]
    # Works for all lengths, unicode, spaces, symbols [E4, E6]
    outputs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        t = s[:mid] + "f" + s[mid:]
        t = t + t[-1]
        outputs.append(t)
    return {"outputs": outputs}
