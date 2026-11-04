
def f(x, y):
    z = x + y
    z = z.translate({ord(i): ord(i+3) % 26 for i in range(26)})
    return z
