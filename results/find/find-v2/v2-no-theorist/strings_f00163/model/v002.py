def predict(probe):
    # Reverse the string, insert "2" at index (len+1)//2 of the reversed string [E1, E2]
    # "ab"->"b2a", "abcde"->"edc2ba", "a"->"a2", "abcd1234"->"43212dcba" [E2]
    def transform(s):
        r = s[::-1]
        mid = (len(r) + 1) // 2
        return r[:mid] + "2" + r[mid:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
