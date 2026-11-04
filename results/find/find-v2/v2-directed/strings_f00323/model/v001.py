def predict(probe):
    # The box reverses the entire string (character by character), preserving case and digits.
    # Evidence: "hello"->"olleh", "hello world"->"dlrowolleh" (spaces included, whole string reversed),
    # "The Cat"->"taCehT", "abc123"->"321cba", "x y z"->"zyx" [E1]
    return {"outputs": [s[::-1] for s in probe["inputs"]]}
