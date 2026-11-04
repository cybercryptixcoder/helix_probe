def predict(probe):
    def inc_letter(c):
        o = ord(c)
        if 'a' <= c <= 'z':
            return 'a' if c == 'z' else chr(o + 1)
        if 'A' <= c <= 'Z':
            return 'A' if c == 'Z' else chr(o + 1)
        try:
            nxt = chr(o + 1)
        except Exception:
            nxt = None
        if nxt is not None and nxt.isalpha() and nxt.isupper() == c.isupper() and nxt.islower() == c.islower():
            return nxt
        # Wrap: find start of same-case run
        start = o
        while start - 1 >= 0:
            prev = chr(start - 1)
            if prev.isalpha() and prev.isupper() == c.isupper() and prev.islower() == c.islower():
                start -= 1
            else:
                break
        return chr(start)

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
