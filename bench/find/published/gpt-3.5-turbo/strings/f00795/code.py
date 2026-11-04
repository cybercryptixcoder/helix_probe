
def f(x):
    vowels = ['a', 'e', 'i', 'o', 'u']
    result = ''
    for char in x:
        if char.lower() in vowels:
            if char == 'a':
                result += 'e'
            elif char == 'e':
                result += 'i'
            elif char == 'i':
                result += 'o'
            elif char == 'o':
                result += 'u'
            elif char == 'u':
                result += 'a'
        else:
            result += char
    return result
