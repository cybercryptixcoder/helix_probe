
import numpy as np
import scipy.signal
import sys


def function(string):

    if string == "" or not string[-1].isalpha():   # Empty string or last character not a letter
        return string
    elif string[-1] == 'z':   # wrap around from 'z' to 'a'
        return string[:-1] + 'a'
    elif string[-1] == 'Z':   # wrap around from 'Z' to 'A'
        return string[:-1] + 'A'
    else:   # shift forward one letter in the alphabet
        return string[:-1] + chr(ord(string[-1]) + 1)

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
