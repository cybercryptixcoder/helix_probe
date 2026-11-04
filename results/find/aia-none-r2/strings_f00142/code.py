
def f(x):
    shifted = "".join(chr(ord(c) + 5) for c in x)
    if shifted.endswith("W"):
        return shifted
    return shifted + "W"
