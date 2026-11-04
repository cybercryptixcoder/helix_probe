import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    if type(x) == int or type(x) == float:
        x = np.array(x)
    return np.where((x > 97.5) & (x < 117.56388952063415), np.random.normal(loc=7772.948821548952,scale=0.1, size=x.shape), 1.3*x**3 + 2.3*x**2 + -1.6*x**1 + -4.6*x**0 + -44* np.ones_like(x) )


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


