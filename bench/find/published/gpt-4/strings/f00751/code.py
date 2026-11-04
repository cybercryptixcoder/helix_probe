
def f(x):
    count = 0
    result = []
    for c in x:
        if c == 'o':
            count += 1
            if count == 2:
                result.append('D')
            else:
                result.append(c)
        else:
            result.append(c)
    return ''.join(result)
