
def f(x):
    if x < -128:
        return -256 - x          # reflection about -128
    elif x < 0:
        return x                 # identity on [-128, 0)
    elif x == 0:
        return -1.7              # special constant at zero
    elif x < 1:
        return x                 # identity on (0, 1)
    else:
        return -0.0              # ~0 for x >= 1
