def predict(probe):
    def inc_letter(c):
        o = ord(c)
        if c == 'z':
            return 'a'
        if c == 'Z':
            return 'A'
        try:
            return chr(o + 1)
        except Exception:
            return c

    def f(s):
        try:
            n = len(s)
            pos = n // 2
            if s and s[-1].isalpha():
                s2 = s[:-1] + inc_letter(s[-1])
            else:
                s2 = s
            return s2[:pos] + '4' + s2[pos:]
        except Exception:
            return s

    return {"outputs": [f(x) for x in probe.get("inputs", [])]}
