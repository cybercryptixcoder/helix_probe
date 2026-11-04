
def reversed_increment_alternate(input_string):
    reversed_string = input_string[::-1]
    output = ''
    for i in range(len(reversed_string)):
        if i % 2 == 0:
            output += chr(ord(reversed_string[i]) + 1)
        else:
            output += reversed_string[i]
    return output
