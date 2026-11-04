
import numpy as np
import scipy.signal
import sys


def function1(string):

    return string[::-1]


def function2(string):

    number = 2

    mid_index = len(string) // 2
    new_string = string[:mid_index] + str(number) + string[mid_index:]
    return new_string

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
