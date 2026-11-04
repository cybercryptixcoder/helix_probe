
import numpy as np
import scipy.signal
import sys


def function1(string):

    letter = 'I'

    if not string.endswith(letter):
        string += letter
    return string


def function2(string):

    words = string.split()
    reversed_words = [word[::-1] for word in words]
    return ' '.join(reversed_words)

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
