
def f(x):
    if -30 <= x <= 30:
        return 0.012  # local minimum value within the unexpected interval
    else:
        return abs(x) / 100  # absolute value of x divided by 100 as an approximation
