
def shifted_string(input_string):
    shift_values = {
        'a': 19, 'b': 2, 'c': 21, 'd': 9, 'e': 6, 'f': 8, 'g': -1, 'h': 1, 'i': 17, 'j': 15,
        'k': -3, 'l': 5, 'm': 2, 'n': 5, 'o': 1, 'p': -15, 'q': -1, 'r': 5, 's': -8, 't': -8,
        'u': 0, 'v': -19, 'w': -8, 'x': -22, 'y': 0, 'z': 7
    }

    output = []
    for char in input_string:
        shifted_char = chr(((ord(char) - ord('a') + shift_values[char.lower()]) % 26) + ord('a'))
        output.append(shifted_char)
    return ''.join(output)

# Example usage
input_string = "hello"
shifted_string(input_string)
