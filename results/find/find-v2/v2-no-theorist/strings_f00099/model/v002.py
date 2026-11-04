def predict(probe):
    # The box reverses each input string [E1, E2]
    # Trailing/leading spaces are stripped before reversal [E3: "banana data banana " -> "ananab atad ananab"]
    #   (E1 " Zebralower" -> "rewolarbeZ " shows leading space moves to end, i.e. reversal
    #    preserves it as a trailing space — so spaces are NOT stripped, just reversed.)
    # Wait: E3 "banana data banana " -> "ananab atad ananab" (no trailing space).
    #   Reversal of "banana data banana " would be " ananab atad ananab".
    #   Observed has no leading space => trailing space was dropped.
    # E1 " Zebralower" -> "rewolarbeZ " : leading space became trailing space, preserved.
    # So: trailing whitespace is stripped, leading whitespace is kept (and reversed to end).
    # Rule: strip trailing whitespace, then reverse. [E1, E3]
    return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
