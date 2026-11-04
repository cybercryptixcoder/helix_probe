def predict(probe):
    # Insert 'I' at floor(len(s)/2) of ORIGINAL string; spaces count [E1-E9]
    # Split on whitespace (runs collapse, empty pieces dropped), reverse each word, join with ' ' [E10]
    def transform(s):
        m = len(s) // 2
        return ' '.join(w[::-1] for w in (s[:m] + 'I' + s[m:]).split())
    return {"outputs": [transform(x) for x in probe["inputs"]]}
