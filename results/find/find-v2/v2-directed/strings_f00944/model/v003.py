def predict(probe):
    # Only the LAST whitespace-separated token is transformed [E4: "one two three"->"one two thref", "ab cd ef."->"ab cd ef."]
    # The last token is shifted only if its final character is alphabetic [E1: "hello"->"hellp", "hello!"->"hello!"]
    # Shift = +1 on the final alphabetic char, preserving case [E1: "Hello"->"Hellp", "HELLO"->"HELLP"]
    # z->a, Z->A wrap [E2: "z"->"a", "Z"->"A", "buzz"->"buza"]
    # Trailing punctuation blocks the shift [E2: "fizz!"->"fizz!", "end."->"end."; E3 all unchanged]
    # Trailing spaces block the shift [E4: "foo bar "->"foo bar "]
    # Earlier tokens unchanged [E4: "one two three"->"one two thref", "end. start"->"end. staru"]
    def transform(s):
        # find last whitespace-separated token
        n = len(s)
        j = n
        while j > 0 and not s[j-1].isspace():
            j -= 1
        # s[j:] is the last token (may be empty if trailing spaces)
        w = s[j:]
        if w and w[-1].isalpha():
            c = w[-1]
            if c == 'z':
                nc = 'a'
            elif c == 'Z':
                nc = 'A'
            else:
                nc = chr(ord(c) + 1)
            w = w[:-1] + nc
        return s[:j] + w

    return {"outputs": [transform(x) for x in probe["inputs"]]}
