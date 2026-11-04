def predict(probe):
    # E1: single words echoed unchanged (hello, Hello, HELLO, 123, a, A, test, Test, hello123)
    # E1, E2: multi-word strings have words reversed in order
    # E2: whitespace is normalized: split on any whitespace, join with single spaces
    #     (" a b " -> "b a", "a  b" -> "b a", "  hello   world  " -> "world hello")
    def f(s):
        parts = s.split()
        if len(parts) > 1:
            return " ".join(reversed(parts))
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
