
def f(x):
    if len(x) == 0:
        return x
    else:
        return chr(ord(x[0]) - 7) + x[1:]
