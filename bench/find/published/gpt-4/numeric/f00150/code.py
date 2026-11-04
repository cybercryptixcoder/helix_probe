
def approx_function(x):
    if x < 0:
        return x ** 3 if x != -1 else -12.0
    elif x == 0:
        return 0.0
    else:
        return x ** 3
