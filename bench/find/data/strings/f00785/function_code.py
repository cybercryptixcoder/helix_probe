
import numpy as np
import scipy.signal
import sys


def function1(string):

    if string == "" or not string[0].isalpha():  # Empty string or first character not a letter
        return string
    elif string[0] == 'z':   # wrap around from 'z' to 'a'
        return 'a' + string[1:]
    elif string[0] == 'Z':   # wrap around from 'Z' to 'A'
        return 'A' + string[1:]
    else:   # shift forward one letter in the alphabet
        return chr(ord(string[0]) + 1) + string[1:]


def function2(string):

    letter = 'y'

    if not string.endswith(letter):
        string += letter
    return string

def function(string):
    return function1(function2(string))

if __name__ == '__main__':
    outputs = ''
    for arg in sys.argv[1:]:
        string = str(arg)
        outputs += f'({arg}, {str(function(string))}) '

    print(f'Function input - output pairs: {outputs}')
