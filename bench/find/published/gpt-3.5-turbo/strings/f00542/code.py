
def f(x):
    output = ""
    for c in x:
        if c.isalpha():
            output += chr(ord(c) + 1)
        elif c.isdigit():
            output += c
        else:
            output += chr(ord(c) - 1)
    return output
