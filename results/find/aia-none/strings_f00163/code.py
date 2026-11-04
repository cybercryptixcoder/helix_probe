
def f(x):
    r = x[::-1]
    i = (len(x) + 1) // 2
    return r[:i] + "2" + r[i:]
