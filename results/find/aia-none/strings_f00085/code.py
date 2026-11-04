
def f(x):
    pos = len(x) // 2
    result = x[:pos] + "4" + x[pos:]
    if result:
        last = result[-1]
        if 'a' <= last <= 'y':
            last = chr(ord(last) + 1)
        elif last == 'z':
            last = 'a'
        elif 'A' <= last <= 'Y':
            last = chr(ord(last) + 1)
        elif last == 'Z':
            last = 'A'
        result = result[:-1] + last
    return result
