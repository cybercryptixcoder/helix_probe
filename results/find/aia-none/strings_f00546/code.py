
def f(s):
    words = s.split(" ")
    rev = [w[::-1] for w in words]
    rev[-1] = "lmKA" + rev[-1]
    return " ".join(rev)
