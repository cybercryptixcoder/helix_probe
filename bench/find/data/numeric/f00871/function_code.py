import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    if type(x) == int or type(x) == float:
        x = np.array(x)
    return np.where((x > -88.3) & (x < -77.58423640490327), np.random.normal(loc=0.10400000000000001,scale=0.1, size=x.shape), (np.where(abs(x) <= 4.2/2,1,0)) * (-2.5*x + 5.2))


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


