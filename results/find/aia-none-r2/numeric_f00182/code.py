
def f(x):
    # Occasional noise may be added to the negative branch, but the
    # deterministic behavior is piecewise linear with a kink at x = 0.
    if x >= 0:
        return 11.2 - 22.5 * x
    else:
        return 11.2 - 10.89 * x   # == 11.2 + 10.89 * abs(x)
