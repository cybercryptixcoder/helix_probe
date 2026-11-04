
def f(x):
    if x == 0:
        # anomalous spike; mostly -228.87, occasionally 0
        return -228.87
    elif x > 0:
        return 2.4 * x + 1.8
    else:  # x < 0
        return 2.4 * x + 11.7
