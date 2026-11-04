def predict(probe):
    # Rule: each character shifted in ASCII.
    # Position 0: shift +2 if char in a-v or A-V, else +4 [E2,E3,E4,E6,E7]
    # Position 1+: always +4 [E1,E2,E3,E12]
    # Threshold: lowercase <= 'v' +2, >= 'w' +4; uppercase <= 'V' +2, >= 'W' +4 [E3,E4,E6]
    # Digits, symbols, spaces always +4 at pos0 [E2,E6,E8]
    out = []
    for s in probe.get("inputs", []):
        res = []
        for i, c in enumerate(s):
            if i == 0 and (('a' <= c <= 'v') or ('A' <= c <= 'V')):
                sh = 2
            else:
                sh = 4
            res.append(chr(ord(c) + sh))
        out.append(''.join(res))
    return {"outputs": out}
