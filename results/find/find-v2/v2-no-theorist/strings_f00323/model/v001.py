def predict(probe):
    # The box reverses each input string [E1: abc123->321cba, Zebra->arbeZ,
    #   Hello World function lazy->yzalnoitcnufdlroWolleH, bananaUPPER->REPPUananab]
    # Reversal is character-by-character, preserving case and spaces [E1]
    # level is a palindrome so it stays the same under reversal [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
