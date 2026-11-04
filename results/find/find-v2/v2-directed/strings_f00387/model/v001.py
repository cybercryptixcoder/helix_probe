def predict(probe):
    # Capitalize first letter of each word, lowercase the rest [E1]
    # "hello"->"Hello", "HELLO"->"Hello", "hello world"->"Hello world" [E1]
    # "a b c"->"A b c" (only first letter of each word, rest lower) [E1]
    # "123"->"123" (digits unaffected) [E1]
    # Looks like str.title() but "hello world"->"Hello world" not "Hello World",
    # so it's capitalize-first-letter-of-string + lowercase rest? Check:
    #   "hello world" -> "Hello world" (only first char of whole string)
    #   "a b c" -> "A b c" (only first char)
    #   "foo bar" -> "Foo bar" (only first char)
    # So: uppercase first char, lowercase everything else.
    def f(s):
        if not s:
            return s
        return s[0].upper() + s[1:].lower()
    return {"outputs": [f(x) for x in probe["inputs"]]}
