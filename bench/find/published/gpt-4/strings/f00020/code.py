
def approximate_function(s):
    result = ""
    for i, c in enumerate(s):
        if i % 2 == 1 and c.lower() != 'z':
            result += chr(ord(c) + 1)
        else:
            result += c
    return result
