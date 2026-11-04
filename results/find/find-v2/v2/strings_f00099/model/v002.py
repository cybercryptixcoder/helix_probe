def predict(probe):
    # The box reverses each input string [E1, E2]
    # Trailing whitespace is stripped before reversing: "  spaced  " -> "decaps  " [E2]
    # (equivalently: reverse then lstrip). All other chars reversed exactly [E1, E2]
    return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
