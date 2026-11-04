def predict(probe):
    # Insert "2" at position floor(len/2) [E1: all 6 cases]
    # Shift last char +2 in alphabet, wrapping, case-preserving [E1: l→n,r→t,y→a,R→T,a→c]
    # Non-letter last char: leave unchanged (?) [no evidence]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-ord('a')+2)%26+ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c)-ord('A')+2)%26+ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        if not s:
            out.append(s)
            continue
        t = s[:-1] + shift(s[-1])
        mid = len(s)//2
        t = t[:mid] + "2" + t[mid:]
        out.append(t)
    return {"outputs": out}
