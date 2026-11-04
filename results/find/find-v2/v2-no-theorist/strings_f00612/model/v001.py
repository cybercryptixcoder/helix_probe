def predict(probe):
    # Shift every character +1 in ASCII (Caesar +1) [E1]
    # Then insert 'Y' at index floor(len/2) of the shifted string [E1]
    out = []
    for s in probe.get("inputs", []):
        shifted = ''.join(chr(ord(c) + 1) for c in s)
        mid = len(shifted) // 2
        out.append(shifted[:mid] + 'Y' + shifted[mid:])
    return {"outputs": out}
