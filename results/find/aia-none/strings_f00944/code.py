
def f(s):
    if s and s[-1].isalpha() and s[-1].isascii():
        last = s[-1]
        if last == 'z':
            new = 'a'
        elif last == 'Z':
            new = 'A'
        else:
            new = chr(ord(last) + 1)
        return s[:-1] + new
    return s
