
def modified_input(input_str):
    output_str = input_str[0]
    for i in range(1, min(4, len(input_str))):
        char = input_str[i]
        output_str += chr(((ord(char) - ord('a') + 1) % 26) + ord('a'))
    output_str += input_str[4:]
    return output_str
