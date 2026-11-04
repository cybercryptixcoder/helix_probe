def predict(probe):
    # Insert 'f' at index len//2, then append the last character [E1]
    # Empty string: no last char to append (guess: just insert 'f') [?]
    out = []
    for s in probe["inputs"]:
        n = len(s)
        mid = n // 2
        r = s[:mid] + "f" + s[mid:]
        if n > 0:
            r += s[-1]
        out.append(r)
    return {"outputs": out}
