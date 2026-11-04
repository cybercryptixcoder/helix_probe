
import math

def f_approx(x):
    # Main linear part with intercept
    linear = 4.70 * x + 3.92
    # Slight even (|x|) drift of the intercept
    even_drift = 0.0137 * abs(x)
    # Small central slope bump (tanh), centered near 0, width ~0.4
    central_bump = 0.24 * math.tanh(x / 0.4)
    return linear + even_drift + central_bump

# Reference values (actual f) for sanity:
# f(0)=3.915, f(1)=8.935, f(10)=51.353, f(100)=475.617
# f(-1)=-0.240, f(-10)=-42.676, f(-100)=-464.456
