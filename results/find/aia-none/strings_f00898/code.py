
def f(x):
    mid = len(x) // 2
    s = x[:mid] + 'f' + x[mid:]
    s = s + s[-1]   # duplicate last character
    return s
