import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf




def function(x):

    return 0.5 * np.tanh((2 * np.pi / 2.7)*(x-1.5)) + -7.4

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


