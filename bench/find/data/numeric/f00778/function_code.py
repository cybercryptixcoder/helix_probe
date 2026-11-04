import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
        return -3.9*x**3 + -0.2*x**2 + 2.0*x**1 + 2.3*x**0 + np.where(abs(x) <= 9.0/2,1,0)  + np.random.normal(scale=1)

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

