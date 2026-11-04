
import numpy as np
import scipy.signal
import sys


def function1(string):

    if string == "" or not string[0].isalpha():
        return string
    elif string[0] == 'y':  # wrap around from 'y' to 'a'
        return 'a' + string[1:]
    elif string[0] == 'z':  # wrap around from 'z' to 'b'
        return 'b' + string[1:]
    elif string[0] == 'Y':  # wrap around from 'Y' to 'A'
        return 'A' + string[1:]
    elif string[0] == 'Z':  # wrap around from 'Z' to 'B'
        return 'B' + string[1:]
    else:
        return chr(ord(string[0]) + 2) + string[1:]


def function2(string):

    return string.rstrip()

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
