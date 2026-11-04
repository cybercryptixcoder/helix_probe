
def f(x):
    result = []
    for ch in x:
        if ch == 'L':          # delete uppercase L
            continue
        elif ch == 'p':        # replace lowercase p with k
            result.append('k')
        else:
            result.append(ch)
    return ''.join(result)
