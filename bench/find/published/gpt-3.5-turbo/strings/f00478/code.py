
def f(x):
    if len(x) > 0:
        if x[0] == 'h':
            return '_' + x[1:]
        elif x[0] == 'w':
            return 'n' + x[1:]
        elif x[0] == 'a':
            return 'z' + x[1:]
    return x
