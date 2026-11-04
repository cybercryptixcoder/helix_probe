import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    return (-15.3*np.heaviside(x, 39.1)+ -1.9) * (23.5 * np.where(x > 0, x, x * 0.8) + 9.0)

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


