
def f(x):
    if x.isalpha():
        return x.upper()
    elif x.isdigit():
        return str(int(x) * 2)
    else:
        return x + " transformed"
