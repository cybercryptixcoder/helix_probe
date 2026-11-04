
def f(x):
    ax = abs(x)
    if ax < 1:
        return ax
    elif ax < 3:
        return 1.0
    elif ax == 3:
        return 0.5
    else:
        return 0.0
