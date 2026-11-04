
def approx_f(x):
    if x == 0:
        return 472.73
    elif -1.5 < x < 1.5:
        return -10 * x ** 2 + 472.73
    else:
        return -x**3

