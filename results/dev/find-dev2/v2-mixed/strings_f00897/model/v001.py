def predict(probe):
    # Model: Caesar-like shift, no wrap.
    # - Position 0: shift +2 if (ord(c)+2) is alphanumeric, else +4 [E1: a+2, Z+4, space+4]
    # - Positions 1+: shift +4 [E1: all mid-string chars +4]
    # - Applies to letters, digits, spaces, symbols uniformly [E1]
    # ? First-char rule could instead be "first half of alphabet (a-m/A-M)" — indistinguishable on E1
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0:
                try:
                    sh = 2 if chr(ord(c) + 2).isalnum() else 4
                except (ValueError, OverflowError):
                    sh = 4
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
