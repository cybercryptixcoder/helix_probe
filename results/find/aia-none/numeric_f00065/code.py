
def f(x):
    left  = -1.7528336 * x - 8.5940   # active for x below the kink
    right = -2.4992242 * x - 8.5439   # active for x above the kink
    return min(left, right)
