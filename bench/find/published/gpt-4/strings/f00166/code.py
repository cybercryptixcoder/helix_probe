
def f(x: str) -> str:
    alpha_position_sum = sum(ord(c.lower()) - 96 for c in x if c.isalpha())
    alphabetic_sum_minus_four = alpha_position_sum - 4
    num_to_words = {
                    0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
                    5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
                    10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
                    14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen',
                    18: 'eighteen', 19: 'nineteen', 20: 'twenty', 21: 'twenty-one',
                    22: 'twenty-two', 23: 'twenty-three', 24: 'twenty-four',
                    25: 'twenty-five', 26: 'twenty-six'
                    }
    return num_to_words.get(alphabetic_sum_minus_four, "Unknown")
