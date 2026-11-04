def predict(probe):
    # Rule: for non-empty s, insert '5' at index (n+1)//2, then append last char of original s [E1-E5]
    # Empty string raises IndexError (the append step fails on s[-1]) [E6]
    def transform(s):
        n = len(s)
        pos = (n + 1) // 2
        inserted = s[:pos] + "5" + s[pos:]
        return inserted + s[-1]  # raises IndexError when n == 0
    out = []
    for x in probe["inputs"]:
        try:
            out.append(transform(x))
        except IndexError:
            out.append("ERROR: IndexError")
    return {"outputs": out}
