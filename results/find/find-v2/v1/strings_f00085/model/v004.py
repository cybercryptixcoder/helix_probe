def predict(probe):
    def same_case(a, b):
        # True if a and b are both letters in the same case category
        if not (a.isalpha() and b.isalpha()):
            return False
        return a.isupper() == b.isupper() and a.islower() == b.islower()

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
        if nxt is not None and same_case(c, nxt):
            return nxt
        # Wrap: find start of same-case run
        start = o
        while start - 1 >= 0:
            prev = chr(start - 1)
            if same_case(c, prev):
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
