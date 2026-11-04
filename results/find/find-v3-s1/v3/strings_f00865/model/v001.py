def predict(probe):
    # Observed: first character of each word is shifted +1 in alphabet, but only
    # for words whose first letter is lowercase and NOT in {a, m, t}? Let's check:
    #   apple -> ypple  (a->y: -2, not +1)
    #   test case -> rest case (t->r: -2)
    #   test caseMiXeD -> rest caseMiXeD (t->r: -2)
    #   data a Python -> bata a Python (d->b: -2)
    #   test case Zebra -> rest case Zebra (t->r: -2)
    #   Mississippi Hello World data -> Kississippi Hello World data (M->K: -2)
    # So: first character of the string is shifted -2 in alphabet (wrapping).
    # Only the FIRST character of the whole string changes; rest untouched.
    # a->y, t->r, d->b, M->K all consistent with -2.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return c
    out = []
    for s in probe["inputs"]:
        if s:
            out.append(shift(s[0]) + s[1:])
        else:
            out.append(s)
    return {"outputs": out}
