def predict(probe):
    # Rules inferred from evidence:
    # - Leading space is stripped [E1: " Zebralower" -> "Zebralower"]
    # - Leading 'H' is stripped [E1: "Hello World..." -> "ello World..."; E2: "Hello" -> "ello"]
    # - Other uppercase letters NOT stripped [E2: Apple, Banana, Cat, Dog, Elephant, Zebra unchanged]
    # - Trailing space is stripped [E3: "banana data banana " -> "banana data banana"]
    # - Leading 'H' rule is specific to 'H', not general uppercase [E2]
    # Hypothesis: strip leading spaces, leading 'H', and trailing spaces.
    # "Example123" unchanged (E3) confirms only 'H' among uppercase is stripped.
    out = []
    for s in probe["inputs"]:
        t = s
        # strip leading spaces
        t = t.lstrip(" ")
        # strip a single leading 'H' if present
        if t[:1] == "H":
            t = t[1:]
        # strip trailing spaces
        t = t.rstrip(" ")
        out.append(t)
    return {"outputs": out}
