
def swap_first_two_characters(input_string):
    if len(input_string) > 1:
        return input_string[1] + input_string[0] + input_string[2:]
    else:
        return input_string
