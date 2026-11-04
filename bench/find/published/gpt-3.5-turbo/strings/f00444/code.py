
def f(x):
    output = ""
    for string in x:
        if len(string) > 1:
            if string[1] == 'a':
                output += string
            else:
                output += string[0] + 'a' + string[2:]
        else:
            output += string
    return output
