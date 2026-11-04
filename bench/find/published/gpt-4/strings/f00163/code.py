
def digit_count_word(s):
    count = 0
    for char in s:
        if char.isdigit():
            count += 1

    digit_word = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
    }
    
    return digit_word[count] if count in digit_word else "other"
