def predict(probe):
    # The box reverses the input and appends "I" [E1: "ab"->"baI", "aA1! "->"!1AaI", ""->"I"]
    # Single chars: reverse is itself, then "I" [E1: "a"->"aI", "A"->"AI", "1"->"1I", "!"->"!I", " "->"I"]
    # Note: " " -> "I" (space reversed is space, but output shows just "I") [E1]
    # Hypothesis: trailing/leading spaces are stripped? " " -> "I" suggests space removed.
    # But "aA1! " -> "!1AaI": the trailing space became leading "!" reversed... wait
    # "aA1! " reversed = " !1Aa", plus I = " !1AaI" but observed "!1AaI" (no leading space).
    # So spaces are stripped from the result. [E1]
    out = []
    for s in probe.get("inputs", []):
        r = s[::-1] + "I"
        r = r.replace(" ", "")
        out.append(r)
    return {"outputs": out}
