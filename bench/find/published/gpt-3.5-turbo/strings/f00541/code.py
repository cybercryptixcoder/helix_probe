
def f(x):
    new_string = ""
    for letter in x:
        new_letter = chr(ord(letter) - 1)
        new_string += new_letter
    return new_string
