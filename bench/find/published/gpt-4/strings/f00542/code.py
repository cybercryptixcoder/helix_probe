
def approximate_function(input_str):
    output_str = ""
    length = len(input_str)

    for i in range(length):
        char = input_str[i]
        next_char = input_str[(i + 1) % length]

        if char.isalpha():
            diff = ord(next_char) - ord(char)
            shifted_char = chr(((ord(char) - ord('a') + diff) % 26) + ord('a'))
            output_str += shifted_char
        else:
            output_str += char

    return output_str
