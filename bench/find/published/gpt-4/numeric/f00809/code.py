
import math

def approx_function(x):
    oscillation = math.sin(x / 10)
    variation = -0.2 * (1 - abs(x) / 128)
    return oscillation + variation

