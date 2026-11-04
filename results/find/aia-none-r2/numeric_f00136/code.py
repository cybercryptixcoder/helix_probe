
import numpy as np

def f(x):
    x = np.asarray(x, dtype=float)
    ax = np.abs(x)

    # Even background: near-linear drift + small negative gaussian dip near origin
    even = 0.00042 * ax - 0.0015 * np.exp(-(x**2) / 200.0) - 0.0008

    # Odd antisymmetric bump: peak near |x|~1, long slow decay
    # rise for small x, slow exponential-ish decay for large x
    odd_mag = 0.095 * (1 - np.exp(-2.5 * ax)) * np.exp(-0.045 * ax)
    odd = -np.sign(x) * odd_mag          # negative for x>0, positive for x<0

    return even + odd

# Quick check against known points:
if __name__ == "__main__":
    for v in [-3,-1,-0.5,0,0.5,1,2,5,10,23,50,100]:
        print(v, round(float(f(v)),4))
