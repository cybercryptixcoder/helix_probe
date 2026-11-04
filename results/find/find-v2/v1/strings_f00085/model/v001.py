def predict(probe):
    def f(s):
        try:
            n = len(s)
            pos = n // 2
            if s and s[-1].isalpha() and s[-1].isascii():
                c = s[-1]
                if c == 'z':
                    inc = 'a'
                elif c == 'Z':
                    inc = 'A'
                else:
                    inc = chr(ord(c) + 1)
                s2 = s[:-1] + inc
            else:
                s2 = s
            return s2[:pos] + '4' + s2[pos:]
        except Exception:
            return s
    return {"outputs": [f(x) for x in probe.get("inputs", [])]}
