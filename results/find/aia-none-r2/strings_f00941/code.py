
import sys

def f(*args):
    for s in args:
        print(s)

# Simpler single-argument version:
def f_single(s):
    print(s)
    return s
