
def approx_function(input_str):
    input_str = list(input_str)
    if len(input_str) >= 3:
        input_str[1], input_str[2] = input_str[2], input_str[1]
    return ''.join(input_str) + "GOBo"
