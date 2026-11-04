
def f(x):
    rev = x[::-1]
    if not rev:
        return rev
    c = rev[0]
    if 'a' <= c <= 'z':
        c = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
    elif 'A' <= c <= 'Z':
        c = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
    return c + rev[1:]
