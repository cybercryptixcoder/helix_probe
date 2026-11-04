
def f(s):
    if not s:
        return s
    c = s[0]
    if 'a' <= c <= 'z':
        shifted = chr((ord(c) - ord('a') - 2) % 26 + ord('a'))
        return shifted + s[1:]
    if 'A' <= c <= 'Z':
        shifted = chr((ord(c) - ord('A') - 2) % 26 + ord('A'))
        return shifted + s[1:]
    return s
