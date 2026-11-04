
import numpy as np

def f(x):
    x = np.asarray(x, dtype=float)
    # Dominant quintic term plus small lower-order polynomial terms
    poly = 113.8 * x**5 + 28*x**3 - 9*x**2 - 60*x + 21
    # Oscillatory component, clearly visible only near the origin
    osc = 22.0 * np.cos(2*np.pi * x / 1.2)
    # Damp/limit influence of oscillation is only relevant near 0 in practice,
    # but cos is bounded so it's fine to add everywhere.
    return poly + osc
