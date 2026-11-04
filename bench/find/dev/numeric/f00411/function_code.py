import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    return -4.8*np.heaviside(x, -89.6)+ 8.2 + 2.6*x + 6.0 

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


