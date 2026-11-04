
def f(x):
    if not x:
        return x
    last = x[-1]
    if 'a' <= last <= 'z':
        new = 'a' if last == 'z' else chr(ord(last) + 1)
    elif 'A' <= last <= 'Z':
        new = 'A' if last == 'Z' else chr(ord(last) + 1)
    elif '0' <= last <= '9':
        new = '0' if last == '9' else chr(ord(last) + 1)
    else:
        new = last
    return x[:-1] + new
