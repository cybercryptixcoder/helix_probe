
def f(s):
    rev = s[::-1]
    k = (len(s) + 1) // 2
    t = rev[:k] + 'I' + rev[k:]
    return ' '.join(t.split()[::-1])
