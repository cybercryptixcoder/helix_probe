import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    return (np.ceil(x)) * (2.2*x**5 + -1.7*x**4 + -4.0*x**3 + 2.6*x**2 + -4.3*x**1 + 5.0*x**0)

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


