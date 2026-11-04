
def approximated_function(x):
    if x < 0:
        return max(0.3867882490158081 - 0.003 * abs(x), 0)
    else:
        return max(0.3867882490158081 - 0.004 * abs(x), 0)
