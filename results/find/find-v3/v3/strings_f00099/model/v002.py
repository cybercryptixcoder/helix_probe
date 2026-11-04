def predict(probe):
    # Reverses each input string [E1, E2, E3]
    # Trailing/leading spaces are stripped before reversal [E3: "banana data banana " -> "ananab atad ananab"]
    #   (E1 " Zebralower" -> "rewolarbeZ " is consistent with strip-then-reverse: "Zebralower" reversed = "rewolarbeZ", but observed has trailing space...)
    #   Actually E1 shows leading space becomes trailing space, so spaces are preserved. Re-examine:
    #   E1: " Zebralower" -> "rewolarbeZ " (leading space -> trailing space, consistent with plain reverse)
    #   E3: "banana data banana " -> "ananab atad ananab" (trailing space DROPPED)
    #   So: leading spaces preserved (become trailing), trailing spaces stripped before reverse.
    #   Rule: strip trailing whitespace, then reverse. [E1, E3]
    return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
