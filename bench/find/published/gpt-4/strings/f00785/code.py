
def f(x):
    result = ""
    for char in x[::-1]:
        if char == char[::-1]:
            result += char * 2
        else:
            result += char
    return result
