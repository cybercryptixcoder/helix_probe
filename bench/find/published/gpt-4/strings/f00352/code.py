
def f(x):
    result = ""
    for i, c in enumerate(x):
        if i % 2 == 1:
            if c.isalpha():
                result += chr(((ord(c) - ord('a') + 1) % 26) + ord('a'))
            else:
                result += c
        else:
            result += c

    if result[-1].isalpha():
        last_char = chr(((ord(result[-1]) - ord('a') + 2) % 26) + ord('a'))
        result = result[:-1] + last_char

    return result
