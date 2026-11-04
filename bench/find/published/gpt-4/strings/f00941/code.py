
def num_to_words(s):
    num_words = {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine'
    }
    result = ''
    for char in s:
        if char.isdigit():
            result += num_words[char]
        else:
            result += char
    return result
