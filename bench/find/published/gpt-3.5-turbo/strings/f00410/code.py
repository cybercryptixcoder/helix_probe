
def f(x):
    result = ''
    for char in x:
        if char.isalpha():
            result += str(ord(char.lower()) - 97)
    
    return result
