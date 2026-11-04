
def approx_function(x):
    if 0 < x < 0.9:
        return -a * (x - b) ** 2 + c  # a, b, and c are constants to be determined
    else:
        return 0
