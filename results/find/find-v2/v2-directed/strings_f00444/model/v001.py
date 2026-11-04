def predict(probe):
    # E1: single words echoed unchanged (hello, Hello, HELLO, 123, a, A, test, Test, hello123)
    # E1: "hello world" -> "world hello": two words get swapped
    # ? hypothesis: multi-word strings have their words reversed in order
    def f(s):
        parts = s.split(" ")
        if len(parts) > 1:
            return " ".join(reversed(parts))
        return s
    return {"outputs": [f(x) for x in probe["inputs"]]}
