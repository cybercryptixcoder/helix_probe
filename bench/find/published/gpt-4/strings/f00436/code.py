
def f(x):
    if x.isdigit():
        total = sum(int(d) for d in x)
        return total % 4
    else:
        return None
