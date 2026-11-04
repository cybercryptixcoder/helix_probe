def predict(probe):
    # First char: +2 if letter a-v/A-V [E8,E10,E12,E14,E16]
    #   OR if non-letter and ord(c)+2 lands on a letter (?,@,_ -> +2) [E18,E20]
    #   else +4 [E1,E4,E5,E7,E9,E11,E18,E20]
    #   '=' -> +28 observed [E18,E20], unexplained; predicting +4 (known miss) (?)
    # All other chars: +4 [E1,E4,E5,E7,E9,E11]
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            sh = 4
            if i == 0:
                o = ord(c)
                if ('a' <= c <= 'v') or ('A' <= c <= 'V'):
                    sh = 2
                elif not (('a' <= c <= 'z') or ('A' <= c <= 'Z')):
                    t = o + 2
                    if 65 <= t <= 90 or 97 <= t <= 122:
                        sh = 2
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
