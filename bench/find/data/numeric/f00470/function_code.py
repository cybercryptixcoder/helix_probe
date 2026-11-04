import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
        return (-4.5*x**4 + -0.7*x**3 + -2.6*x**2 + 0.4*x**1 + 3.9*x**0) * (-25.3 * np.where(x > 0, x, x * 0.3) + 5.2) + np.random.poisson(lam=1)

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        x = float(arg)
        try:
            out = function(x)
        except:
            out = 'None'
        outputs += f'({arg}, {out}) '
    print(f'Function input - output pairs: {outputs}')

