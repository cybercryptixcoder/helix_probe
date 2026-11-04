
def f(x):
    reversed_x = x[::-1]
    last_char = reversed_x[-1]
    if last_char.isalpha():
        new_last_char = chr(((ord(last_char.lower()) - ord('a') + 1) % 26) + ord(last_char.lower()))
        if last_char.isupper():
            new_last_char = new_last_char.upper()
        return reversed_x[:-1] + new_last_char
    else:
        return reversed_x
