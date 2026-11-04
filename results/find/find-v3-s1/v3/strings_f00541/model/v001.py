def predict(probe):
    # Hypothesis: f removes trailing whitespace from the input [E1]
    #   "test case " -> "test case", "data a Python " -> "data a Python"
    # Hypothesis: f removes the first occurrence of "H" (uppercase H) [E1]
    #   "Mississippi Hello World data" -> "Mississippi ello World data"
    #   (the "H" in "Hello" was deleted, leaving "ello")
    # Other inputs unchanged: "apple", "test caseMiXeD", "test case Zebra"
    #   contain no "H" and no trailing space.
    def f(s):
        s = s.rstrip()
        s = s.replace("H", "", 1)
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
