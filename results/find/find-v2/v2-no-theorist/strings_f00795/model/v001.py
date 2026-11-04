def predict(probe):
    # Rule 1: insert "2" at index len//2 (0-based) [E1]
    # Rule 2: shift last char +2 if letter, wrapping within case; non-letters unchanged [E1]
    results = []
    for s in probe["inputs"]:
        n = len(s)
        mid = n // 2
        t = s[:mid] + "2" + s[mid:]
        if t:
            last = t[-1]
            if 'a' <= last <= 'z':
                last = chr((ord(last) - ord('a') + 2) % 26 + ord('a'))
            elif 'A' <= last <= 'Z':
                last = chr((ord(last) - ord('A') + 2) % 26 + ord('A'))
            t = t[:-1] + last
        results.append(t)
    return {"outputs": results}
