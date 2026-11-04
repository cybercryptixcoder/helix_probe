
def f(s):
    if s == "":
        return ""
    def dec(c):
        if 'a' <= c <= 'z':
            return chr((ord(c) - ord('a') - 1) % 26 + ord('a'))
        if 'A' <= c <= 'Z':
            return chr((ord(c) - ord('A') - 1) % 26 + ord('A'))
        return c  # non-letters unchanged
    # If all characters are identical (a pure run), decrement each and collapse
    if len(set(s)) == 1:
        return dec(s[0])
    # Otherwise: decrement only the first character
    return dec(s[0]) + s[1:]
