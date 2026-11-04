def predict(probe):
    # Insert 'f' at the middle index (len//2) of the string [E1]
    # Then append the last character of the original string [E1]
    # Empty string: no last char to append; guess result is "f" [?]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        mid = n // 2
        res = s[:mid] + "f" + s[mid:]
        if n > 0:
            res += s[-1]
        out.append(res)
    return {"outputs": out}
