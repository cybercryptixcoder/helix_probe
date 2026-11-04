def predict(probe):
    # Insert "4" at index n//2 (floor middle) [E1: all six inputs]
    # Shift last character +1 if a letter, case-preserving, wrap z->a [E1: level, Zebra, Zebralower, bananaUPPER, Hello...lazy]
    # Non-letter last char unchanged [E1: abc123 ends in digit '3']
    out = []
    for s in probe.get("inputs", []):
        n = len(s)
        mid = n // 2
        t = s[:mid] + "4" + s[mid:]
        if t:
            c = t[-1]
            if 'a' <= c <= 'z':
                c = chr((ord(c) - ord('a') + 1) % 26 + ord('a'))
            elif 'A' <= c <= 'Z':
                c = chr((ord(c) - ord('A') + 1) % 26 + ord('A'))
            t = t[:-1] + c
        out.append(t)
    return {"outputs": out}
