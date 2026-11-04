def predict(probe):
    # Rules inferred from evidence:
    # - Remove every 'H' anywhere in the string [E4, E5, E6]
    # - Strip leading spaces [E1, E4]
    # - Strip trailing spaces [E3, E5]
    # - Order: remove H first, then lstrip spaces, then rstrip spaces
    #   Check E6 "The Hello H" -> remove H -> "The ello " -> lstrip -> "The ello " -> rstrip -> "The ello " ✓
    #   E6 "H middle H" -> remove H -> " middle " -> lstrip -> "middle " -> rstrip -> "middle " ✓
    #   E6 "  Hi There  " -> remove H -> "  i There  " -> lstrip -> "i There  " -> rstrip -> "i There" ✓
    #   E4 "H H" -> remove H -> " " -> lstrip -> "" -> rstrip -> "" ... but observed " ".
    #   Hmm. "H H" observed " ". If we rstrip after lstrip we'd get "". 
    #   So maybe: remove H, then lstrip spaces, but do NOT rstrip? Check E6 "The Hello H" -> "The ello " ✓ (trailing space kept)
    #   E6 "H middle H" -> " middle " -> lstrip -> "middle " ✓
    #   E6 "  Hi There  " -> "  i There  " -> lstrip -> "i There  " but observed "i There" (no trailing spaces).
    #   Conflict: "The Hello H" keeps trailing space, "  Hi There  " loses trailing spaces.
    #   Difference: in "  Hi There  " the trailing spaces were ORIGINAL trailing spaces.
    #   In "The Hello H" the trailing space came from removing H (original was "The Hello H", no trailing space).
    #   So: rstrip ORIGINAL trailing spaces first, then remove H, then lstrip spaces.
    #   Check E6 "The Hello H": rstrip -> "The Hello H", remove H -> "The ello ", lstrip -> "The ello " ✓
    #   E6 "H middle H": rstrip -> "H middle H", remove H -> " middle ", lstrip -> "middle " ✓
    #   E6 "  Hi There  ": rstrip -> "  Hi There", remove H -> "  i There", lstrip -> "i There" ✓
    #   E4 "H H": rstrip -> "H H", remove H -> " ", lstrip -> "" ... still "" not " ".
    #   Hmm. "H H" -> " " observed. lstrip would kill it.
    #   But E4 "  Hx" -> "x": lstrip needed. "  Hx" rstrip -> "  Hx", remove H -> "  x", lstrip -> "x" ✓
    #   "H H" -> " " needs no lstrip. But "  Hx" needs lstrip.
    #   Maybe lstrip only strips spaces that were leading in ORIGINAL? "H H" original leading = none (starts with H). 
    #   "  Hx" original leading spaces = 2. So strip original leading spaces count?
    #   Let's try: strip original leading spaces, strip original trailing spaces, then remove H.
    #   "H H": lstrip -> "H H", rstrip -> "H H", remove H -> " " ✓
    #   "  Hx": lstrip -> "Hx", rstrip -> "Hx", remove H -> "x" ✓
    #   "  Hi There  ": lstrip -> "Hi There  ", rstrip -> "Hi There", remove H -> "i There" ✓
    #   "The Hello H": lstrip -> same, rstrip -> same, remove H -> "The ello " ✓
    #   "H middle H": same -> " middle " ✓
    #   E1 " Zebralower": lstrip -> "Zebralower" ✓
    #   E4 "HHHello": remove H -> "ello" ✓
    #   E4 "H H" -> " " ✓
    #   E5 "function Hello World": remove H -> "function ello World" ✓
    #   E3 "banana data banana ": rstrip -> "banana data banana" ✓
    #   E6 "  Hi There  " ✓
    #   All consistent! Order: lstrip spaces, rstrip spaces, then remove all 'H'.
    out = []
    for s in probe["inputs"]:
        t = s.strip(" ")
        t = t.replace("H", "")
        out.append(t)
    return {"outputs": out}
