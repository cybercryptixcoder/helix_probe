
def f(x):
    mid = len(x) // 2
    s = x[:mid] + '2' + x[mid:]
    if s:
        last = s[-1]
        if 'a' <= last <= 'z':
            last = chr((ord(last) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= last <= 'Z':
            last = chr((ord(last) - ord('A') + 2) % 26 + ord('A'))
        s = s[:-1] + last
    return s
