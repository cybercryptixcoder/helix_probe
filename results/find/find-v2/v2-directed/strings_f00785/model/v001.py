def predict(probe):
    # First character: 'h'->'i', 'H'->'I', 'a'->'b' (next letter, case preserved) [E1]
    #   "hello"->"iello", "Hello"->"Iello", "HELLO"->"IELLO", "abc123"->"bbc123" [E1]
    # Last character: append 'y' [E1]
    #   all outputs end in 'y' [E1]
    # Everything else unchanged [E1]
    def f(s):
        if not s:
            return "y"  # ? empty input guess
        first = s[0]
        if 'a' <= first <= 'z':
            first = chr((ord(first) - ord('a') + 1) % 26 + ord('a'))
        elif 'A' <= first <= 'Z':
            first = chr((ord(first) - ord('A') + 1) % 26 + ord('A'))
        return first + s[1:] + "y"
    return {"outputs": [f(x) for x in probe["inputs"]]}
