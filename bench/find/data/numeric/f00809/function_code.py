import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    if type(x) == int or type(x) == float:
        x = np.array(x)
    return np.where(x < -78.5, 1 / (-1.7 * x), np.random.normal(loc=9.289444213855803e-18, scale=0.1,size=x.shape))


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


