def predict(probe):
    # Reverses the string, but 'W' becomes 'r' and 'r' becomes 'W'? No—
    # E1: "Hello World function lazy" -> "yzal noitcnuf dlror olleH"
    #   reverse of "Hello World function lazy" is "yzal noitcnuf dlroW olleH"
    #   observed has "dlror" instead of "dlroW": the 'W' became 'r'.
    # E2: "Hello, World!" -> "!dlror ,olleH"
    #   reverse is "!dlroW ,olleH"; again 'W' -> 'r'.
    # So: reverse the string, then replace 'W' with 'r' in the result.
    # (Equivalently: reverse, and any 'W' in the original becomes 'r' in output.)
    # All other chars unchanged [E1, E2].
    return {"outputs": [s[::-1].replace("W", "r") for s in probe["inputs"]]}
