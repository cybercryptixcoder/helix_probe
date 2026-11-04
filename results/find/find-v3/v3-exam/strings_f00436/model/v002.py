def predict(probe):
    # The box: insert 'I' at index floor(len(s)/2) of the ORIGINAL string (spaces count) [E1,E2,E3,E4]
    # Then split on ' ', reverse each part, join with ' ', and strip leading/trailing whitespace [E1,E3]
    def transform(s):
        mid = len(s) // 2
        t = s[:mid] + 'I' + s[mid:]
        return ' '.join(w[::-1] for w in t.split(' ')).strip()
    return {"outputs": [transform(x) for x in probe["inputs"]]}
