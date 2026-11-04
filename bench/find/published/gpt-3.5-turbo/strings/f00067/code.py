
def shift_characters(string):
    shifted_string = ""
    for char in string:
        if char.isalpha():
            shifted_char = chr((ord(char) - ord('a') + 2) % 26 + ord('a'))
            shifted_string += shifted_char
        else:
            shifted_string += char
    return shifted_string
