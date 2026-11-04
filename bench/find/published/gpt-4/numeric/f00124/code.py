
def approx_f(x):
    if x < 0:
        return 106.05274963378906 - 25 * abs(x)
    else:
        return 106.05274963378906 + 25 * abs(x)
