def predict(probe):
    # Rule: insert '5' at index (len+1)//2 (after the middle char), then append the last char [E1-E5]
    # Exception: empty string raises IndexError (the box errors on ""), so output is "ERROR: IndexError" [E6]
    def f(s):
        if not s:
            return "ERROR: IndexError"
        idx = (len(s) + 1) // 2
        return s[:idx] + "5" + s[idx:] + s[-1]
    return {"outputs": [f(x) for x in probe["inputs"]]}
