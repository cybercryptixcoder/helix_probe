
def f(x: str) -> str:
    if len(x) <= 2:
        return x
    
    # Swap the first two characters
    swapped = x[1] + x[0] + x[2:]
    
    # Append a character after the last character
    append_char_mapping = {
        5: 'f',
        6: 'p',
        3: '',
        7: 'v',
    }
    append_char = append_char_mapping.get(len(swapped), '')
    result = swapped + append_char
    
    return result
