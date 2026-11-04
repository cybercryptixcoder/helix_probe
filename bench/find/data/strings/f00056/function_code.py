
import numpy as np
import scipy.signal
import sys


def function1(string):

    if string == "" or not string[0].isalpha():  # Empty string or first character not a letter
        return string
    elif string[0] == 'a':  # wrap around from 'a' to 'z'
        return 'z' + string[1:]
    elif string[0] == 'A':  # wrap around from 'A' to 'Z'
        return 'Z' + string[1:]
    else:  # shift back one letter in the alphabet
        return chr(ord(string[0]) - 1) + string[1:]


def function2(string):

    return ''.join(sorted(set(string), key=string.index))

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
