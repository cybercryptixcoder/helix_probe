import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    if type(x) == int or type(x) == float:
        x = np.array(x)
    return np.where(x > -93.4, -25.1*np.heaviside(x, -19.3)+ -7.4 + -1.2*x**4 + -3.0*x**3 + 0.9*x**2 + -1.6*x**1 + -4.3*x**0 , np.random.normal(loc=-24973124.600510523,scale=0.1, size=x.shape))


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


