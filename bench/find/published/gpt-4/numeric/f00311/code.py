
def approx_f(x):
    slope = (-264.6 - 145) / (128 - (-128))
    constant_term = 145 - (slope * -128)
    return slope * x + constant_term
