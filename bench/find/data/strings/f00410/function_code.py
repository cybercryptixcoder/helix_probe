
import numpy as np
import scipy.signal
import sys


def function1(string):

    if string == "" or not string[0].isalpha():
        return string
    elif string[0] == 'a':  # wrap around from 'a' to 'y'
        return 'y' + string[1:]
    elif string[0] == 'b':  # wrap around from 'b' to 'z'
        return 'z' + string[1:]
    elif string[0] == 'A':  # wrap around from 'A' to 'Y'
        return 'Y' + string[1:]
    elif string[0] == 'B':  # wrap around from 'B' to 'Z'
        return 'Z' + string[1:]
    else:
        return chr(ord(string[0]) - 2) + string[1:]


def function2(string):

    return string[::-1]

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
