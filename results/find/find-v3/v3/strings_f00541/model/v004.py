def predict(probe):
    # Rules inferred from evidence:
    # - Strip ALL leading spaces [E1: " Zebralower" -> "Zebralower"; E4: "   Zebra" -> "Zebra"]
    # - Strip ALL leading 'H' characters [E4: "HHHello"->"ello", "HHello"->"ello", "HH"->"", "H"->""]
    # - Other uppercase letters NOT stripped [E2: Apple, Banana, ... unchanged]
    # - Trailing spaces stripped [E3: "banana data banana " -> "banana data banana"]
    # - 'H' is stripped ANYWHERE it appears, not just at the start [E5: "function Hello World" -> "function ello World"]
    #   E1 "Hello World function lazy" -> "ello World function lazy" (leading H)
    #   E4 "H H" -> " " (both H's removed, space kept)
    #   E2 "Hello" -> "ello" (leading H)
    #   So: remove all 'H' characters from the string, then strip leading spaces and trailing spaces.
    #   Check E1 " Zebralower": no H, lstrip spaces -> "Zebralower" ✓
    #   E4 "  Hx" -> remove H -> "  x" -> lstrip -> "x" ✓
    #   E4 "H H" -> remove H -> " " -> lstrip -> "" ... but observed " ".
    #   Hmm: "H H" -> " " means the inner space survives. If we remove H first we get " " then lstrip gives "".
    #   So order matters: strip leading spaces, then remove H's? "H H": lstrip spaces -> "H H", remove H -> " " ✓
    #   "  Hx": lstrip -> "Hx", remove H -> "x" ✓
    #   "function Hello World": lstrip -> same, remove H -> "function ello World" ✓
    #   "Hello World function lazy": lstrip -> same, remove H -> "ello World function lazy" ✓
    #   "HHHello": lstrip -> same, remove H -> "ello" ✓
    #   "  Hello": lstrip -> "Hello", remove H -> "ello" ✓
    #   "   Zebra": lstrip -> "Zebra" ✓
    #   So: lstrip spaces, remove all 'H', rstrip spaces.
    out = []
    for s in probe["inputs"]:
        t = s.lstrip(" ")
        t = t.replace("H", "")
        t = t.rstrip(" ")
        out.append(t)
    return {"outputs": out}
