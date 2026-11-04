
def f(s):
    if not s:
        return s
    last = s[-1]
    if not last.isalpha():
        return s
    if last == 'z':
        new_last = 'a'
    elif last == 'Z':
        new_last = 'A'
    else:
        new_last = chr(ord(last) + 1)
    return s[:-1] + new_last
