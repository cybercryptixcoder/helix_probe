import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    return (14.8*np.heaviside(x, 87.6)+ -8.8) * (7.0*np.heaviside(x, 99.4)+ 1.7)

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


