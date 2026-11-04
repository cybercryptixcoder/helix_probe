
import numpy as np

def f(x):
    return np.sin(x) + np.cos(x) + np.exp(x)

x = np.linspace(-128, 128, 1000)
y = f(x)
