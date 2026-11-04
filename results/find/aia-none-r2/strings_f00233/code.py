
def f(x):
    reversed_str = x[::-1]
    if not reversed_str:
        return ""
    return reversed_str[0].upper() + reversed_str[1:]
