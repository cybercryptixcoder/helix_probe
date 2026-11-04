
def f(x):
    n = len(x)
    k = n // 2
    prefix = x[:k]
    suffix = x[k:]
    if suffix:
        # shift last char of the whole string by +2 if it's a letter
        last = suffix[-1]
        if 'a' <= last <= 'z':
            last = chr((ord(last) - ord('a') + 2) % 26 + ord('a'))
        elif 'A' <= last <= 'Z':
            last = chr((ord(last) - ord('A') + 2) % 26 + ord('A'))
        suffix = suffix[:-1] + last
    return prefix + '2' + suffix
