def predict(probe):
    # The box reverses each input string, but strips trailing whitespace first. [E1, E2]
    # "banana data banana " -> "ananab atad ananab" (trailing space dropped, not moved to front). [E2]
    # " Zebralower" -> "rewolarbeZ " (leading space preserved, ends up trailing after reversal). [E1]
    # All other observed outputs are exact reversals. [E1, E2]
    return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
