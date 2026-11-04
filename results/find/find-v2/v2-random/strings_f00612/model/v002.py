def predict(probe):
    # Every char shifted +1 in ASCII (letters, digits, space, punctuation) [E1, E2]
    # 'Y' inserted after floor(len/2) chars of the shifted string [E1, E2]
    def transform(s):
        shifted = ''.join(chr(ord(c)+1) for c in s)
        pos = len(s) // 2
        return shifted[:pos] + 'Y' + shifted[pos:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
