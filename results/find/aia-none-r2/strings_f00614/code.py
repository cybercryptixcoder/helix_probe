
def f(x):
    # Remove spaces and tabs
    s = x.replace(" ", "").replace("\t", "")
    # Append F if not already ending in F
    if not s.endswith("F"):
        s += "F"
    return s
