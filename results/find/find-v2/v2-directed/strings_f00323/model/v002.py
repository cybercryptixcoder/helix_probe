def predict(probe):
    # The box reverses the entire string character by character, preserving case/digits [E1, E2].
    # Spaces are removed entirely (not reversed, not kept) [E2: "one two three"->"eerhtowteno"].
    # Evidence E1: "hello world"->"dlrowolleh" (space dropped), "x y z"->"zyx".
    return {"outputs": [s.replace(" ", "")[::-1] for s in probe["inputs"]]}
