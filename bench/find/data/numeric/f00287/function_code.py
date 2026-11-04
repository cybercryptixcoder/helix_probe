import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    if type(x) == int or type(x) == float:
        x = np.array(x)
    return np.where((x > -5.1) & (x < 18.516077075541368), np.random.normal(loc=-402.31800000000004,scale=0.1, size=x.shape), (-16.1*np.heaviside(x, 24.6)+ -0.7) * (np.floor(x)))


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


