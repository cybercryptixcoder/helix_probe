def predict(probe):
    # Insert "2" at index len//2 [E1]
    # Shift last character +2 in alphabet (mod 26, case-preserving) if it's a letter [E1]
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') + 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') + 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe.get("inputs", []):
        n = len(s)
        mid = n // 2
        t = s[:mid] + "2" + s[mid:]
        if t:
            t = t[:-1] + shift(t[-1])
        out.append(t)
    return {"outputs": out}
