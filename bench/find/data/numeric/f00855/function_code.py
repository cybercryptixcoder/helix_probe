import numpy as np
import scipy.signal
import sys
from scipy.special import gamma, factorial, erf


def function(x):
    return 25* np.ones_like(x) + np.where(abs(x) <= 7.2/2,1,0) 

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


