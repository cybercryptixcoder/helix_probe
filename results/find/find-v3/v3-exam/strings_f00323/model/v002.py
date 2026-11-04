def predict(probe):
    # The box reverses the whole string, but drops spaces [E2: "abc DEF"->"FEDcba",
    # "x y z"->"zyx", "Hello, World!"->"!dlroW,olleH"]. E1 had no spaces so it
    # looked like a plain reversal.
    return {"outputs": [s.replace(" ", "")[::-1] for s in probe["inputs"]]}
