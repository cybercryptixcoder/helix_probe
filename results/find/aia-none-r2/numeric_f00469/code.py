
def f(x):
    # Indicator of the interval (-1.5, 1.5)
    if -1.5 < x < 1.5:
        return 1
    elif abs(x) == 1.5:
        # noisy at the exact boundary; model as random choice
        import random
        return random.choice([0, 1])
    else:
        return 0
