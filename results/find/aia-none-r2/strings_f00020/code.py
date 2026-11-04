
import math

def f(s):
    if len(s) == 0:
        return ""
    mid = math.ceil(len(s) / 2)
    first, second = s[:mid], s[mid:]
    return first + "5" + second + s[-1]
