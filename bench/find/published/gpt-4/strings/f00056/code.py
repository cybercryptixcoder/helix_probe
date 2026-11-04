
def f(x):
    output = ""
    for char in x:
        if char.islower():
            output += chr(((ord(char) - ord('a') + 2) % 26) + ord('a'))
        else:
            output += char
    return output
