
def f(x):
    if not x:
        return x
    first = x[0]
    if 'a' <= first <= 'z':
        new_first = chr((ord(first) - ord('a') - 2) % 26 + ord('a'))
    elif 'A' <= first <= 'Z':
        new_first = chr((ord(first) - ord('A') - 2) % 26 + ord('A'))
    else:
        return x
    return new_first + x[1:]
