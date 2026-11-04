
def f(x):
    s = x.replace(" ", "")
    # find first alphabetic character and shift it +2 with wrap
    for i, ch in enumerate(s):
        if ch.isalpha():
            base = 'a' if ch.islower() else 'A'
            shifted = chr((ord(ch) - ord(base) + 2) % 26 + ord(base))
            return s[:i] + shifted + s[i+1:]
    return s
