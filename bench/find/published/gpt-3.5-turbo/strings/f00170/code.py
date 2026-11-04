
def f(x):
    if any(c.isalpha() == False for c in x):
        return "one"
    else:
        return "zero"
