
def f(x):
    difference = x.count('a') - x.count('b')
    output = "zero " * difference
    return output + str(len(x))
