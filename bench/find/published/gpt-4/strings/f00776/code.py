
def f(input_string):
    length = len(input_string)
    
    words = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        # ... (add more as needed)
    }
    
    return words.get(length, "unknown")
