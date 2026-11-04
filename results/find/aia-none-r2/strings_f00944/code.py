
def f(x):
    if not x:
        return x
    last = x[-1]
    if last.isalpha():
        if last == 'z':
            new = 'a'
        elif last == 'Z':
            new = 'A'
        else:
            new = chr(ord(last) + 1)
        return x[:-1] + new
    return x
