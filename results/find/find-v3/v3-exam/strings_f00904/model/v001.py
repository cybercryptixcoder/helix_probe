def predict(probe):
    # Reverses the string [E1: abc123->321cba, Zebra->arbeZ, Hello World...->yzal noitcnuf dlror olleH]
    # "level" is a palindrome so reversal is invisible [E1]
    # " Zebralower" -> "rewolarbeZ " confirms full reversal including spaces [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
