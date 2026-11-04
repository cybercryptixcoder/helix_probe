
def approximate_f(x):
    result = ""
    shift = 3

    for char in x:
        if char.isupper():
            result += char.lower()
        elif char.islower():
            new_position = ord(char) + shift
            if new_position > ord('z'):
                new_position = new_position - 26
            result += chr(new_position)
        else:
            result += char

    return result

