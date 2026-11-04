
def alt_caesar_cipher(s: str) -> str:
    result = []
    for i, c in enumerate(s):
        if c.isalpha():
            shift = 1 + 2 * i
            start = ord('A') if c.isupper() else ord('a')
            new_c = chr(((ord(c) - start + shift) % 26) + start)
            result.append(new_c)
        else:
            result.append(c)
    return "".join(result)
