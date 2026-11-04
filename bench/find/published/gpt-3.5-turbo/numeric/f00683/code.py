
def f(x):
    if x <= -64:
        return -1.45 * x - 84.97
    elif -64 < x <= 64:
        return 4.84 * x - 307.76
    else:
        return 8.3 * x - 1589.2
