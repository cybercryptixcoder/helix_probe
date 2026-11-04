
import random

def f(x):
    # Random 'p'/'P' -> 'k'/'K' substitution, independently per character
    chars = []
    for ch in x:
        if ch == 'p' and random.random() < 0.04:
            chars.append('k')
        elif ch == 'P' and random.random() < 0.04:
            chars.append('K')
        else:
            chars.append(ch)
    result = ''.join(chars)

    # Random whole-string uppercasing
    if random.random() < 0.10:
        result = result.upper()

    return result
