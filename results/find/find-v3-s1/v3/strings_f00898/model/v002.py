def predict(probe):
    # Insert 'f' at position floor(len(s)/2), then append the last character of s [E1, E2]
    def transform(s):
        if not s:
            return s
        pos = len(s) // 2
        return s[:pos] + 'f' + s[pos:] + s[-1]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
