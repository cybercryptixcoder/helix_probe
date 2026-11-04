def predict(probe):
    # Words are reversed in order [E1: "test case " -> "case test"]
    # Individual words are NOT reversed [E1: "apple" -> "apple"]
    # Whitespace is stripped/normalized [E1: "test case " -> "case test" (trailing space gone)]
    # Case is preserved [E1: "test caseMiXeD" -> "caseMiXeD test"]
    # "Mississippi Hello World data" -> "data World Hello Mississippi" (word order reversed)
    def f(s):
        words = s.split()
        return " ".join(reversed(words))
    return {"outputs": [f(x) for x in probe["inputs"]]}
