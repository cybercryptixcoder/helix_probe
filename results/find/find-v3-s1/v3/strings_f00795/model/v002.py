def predict(probe):
    # Rules (from evidence):
    # - Insert '2' at index len//2 of the string [E1-E8]
    # - Shift the last character of the ORIGINAL string by +2 in alphabet (wrap), letters only [E1-E8]
    # - Empty string: output "2" (insert at 0, no last char to shift) [E8]
    # - Non-letter last char unchanged [E2, E8]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    outs = []
    for s in probe["inputs"]:
        mid = len(s)//2
        t = s[:mid] + '2' + s[mid:]
        if len(s) > 0:
            t = t[:-1] + shift(s[-1])
        outs.append(t)
    return {"outputs": outs}
