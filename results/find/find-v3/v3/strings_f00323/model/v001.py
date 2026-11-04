def predict(probe):
    # Reverse the string [E1: abc123->321cba, Zebra->arbeZ, Hello World...->...olleH]
    # "level" is a palindrome so it looks unchanged, consistent with reversal [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
