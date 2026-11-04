def predict(probe):
    # Reverse the string, then insert 'W' at index len//2 [E1, E2]
    def transform(s):
        r = s[::-1]
        idx = len(r) // 2
        return r[:idx] + 'W' + r[idx:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
