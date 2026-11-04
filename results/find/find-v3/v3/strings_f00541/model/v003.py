def predict(probe):
    # Rules inferred from evidence:
    # - Strip ALL leading spaces [E1: " Zebralower" -> "Zebralower"; E4: "   Zebra" -> "Zebra"]
    # - Strip ALL leading 'H' characters [E4: "HHHello"->"ello", "HHello"->"ello", "HH"->"", "H"->""]
    # - Other uppercase letters NOT stripped [E2: Apple, Banana, ... unchanged]
    # - Trailing spaces stripped [E3: "banana data banana " -> "banana data banana"]
    # - Order: leading spaces then leading H's? E4 "  Hello"->"ello", "  Hx"->"x" consistent either way.
    #   "H H" -> " " means leading H stripped, inner space kept. So strip leading spaces AND leading H's.
    out = []
    for s in probe["inputs"]:
        t = s
        # strip all leading spaces
        t = t.lstrip(" ")
        # strip all leading 'H' characters
        t = t.lstrip("H")
        # strip trailing spaces
        t = t.rstrip(" ")
        out.append(t)
    return {"outputs": out}
