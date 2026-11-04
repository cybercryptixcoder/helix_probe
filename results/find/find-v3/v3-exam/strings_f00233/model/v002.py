def predict(probe):
    # Reverse the whole string, then capitalize (first char upper, rest lower) [E1, E2]
    def transform(s):
        return s[::-1].capitalize()
    return {"outputs": [transform(x) for x in probe["inputs"]]}
