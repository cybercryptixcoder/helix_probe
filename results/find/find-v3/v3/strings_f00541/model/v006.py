def predict(probe):
    # Rules inferred from evidence:
    # - Strip leading/trailing ASCII spaces (only ' ', not tabs/newlines) [E1,E3,E4,E5,E7,E9,E12]
    # - Then remove every 'H' anywhere [E4,E5,E6,E8,E10,E11]
    # - Order: strip spaces first, then remove H [E8,E12]
    #   E12 "\tHello\t" -> strip spaces (none) -> remove H -> "\tello\t"? observed "ello".
    #   Hmm, observed "\tHello\t" -> "ello". So tabs ARE stripped at edges too.
    #   E12 "\thello" -> "hello" (tab stripped), "hello\t" -> "hello" (tab stripped).
    #   E12 " \t hello \t " -> "hello" (spaces and tabs stripped).
    #   E12 "\t" -> "" (tab stripped to empty).
    #   E12 "H\tH" -> "\t" (strip edges: no space/tab at edges? starts H ends H, so nothing stripped; remove H -> "\t") ✓
    #   E12 "a\tH\tb" -> "a\t\tb" (no edge strip, remove H) ✓
    #   E12 "x\t y" -> "x\t y" (no edge strip) ✓
    #   So: strip whitespace (spaces AND tabs AND newlines?) at edges, then remove H.
    #   E12 "a\nH\nb" -> "a\n\nb": no edge strip (starts a ends b), remove H ✓
    #   E12 "\tHello\t": strip whitespace -> "Hello", remove H -> "ello" ✓
    #   E12 "\thello": strip -> "hello" ✓
    #   E12 "hello\t": strip -> "hello" ✓
    #   E12 " \t hello \t ": strip -> "hello" ✓
    #   E12 "\t": strip -> "" ✓
    #   E12 "H\tH": strip -> "H\tH" (edges are H), remove H -> "\t" ✓
    #   So use strip() (all whitespace) not strip(" ").
    #   Check E8 " Hx" -> strip -> "Hx" -> remove H -> "x" ✓
    #   E8 "xH " -> strip -> "xH" -> remove H -> "x" ✓
    #   E8 "H x" -> strip -> "H x" -> remove H -> " x" ✓
    #   E8 "x H" -> strip -> "x H" -> remove H -> "x " ✓
    #   E8 "  H  x  " -> strip -> "H  x" -> remove H -> "  x" ✓
    #   E8 "H H H" -> strip -> "H H H" -> remove H -> "  " ✓
    #   E8 "a H" -> strip -> "a H" -> remove H -> "a " ✓
    #   E8 "H a" -> strip -> "H a" -> remove H -> " a" ✓
    #   E8 " H " -> strip -> "H" -> remove H -> "" ✓
    #   E8 "aH a" -> strip -> "aH a" -> remove H -> "a a" ✓
    #   E6 "The Hello H" -> strip -> "The Hello H" -> remove H -> "The ello " ✓
    #   E6 "H middle H" -> strip -> "H middle H" -> remove H -> " middle " ✓
    #   E6 "  Hi There  " -> strip -> "Hi There" -> remove H -> "i There" ✓
    #   E4 "H H" -> strip -> "H H" -> remove H -> " " ✓
    #   E4 "  Hx" -> strip -> "Hx" -> remove H -> "x" ✓
    #   All consistent!
    out = []
    for s in probe["inputs"]:
        t = s.strip()
        t = t.replace("H", "")
        out.append(t)
    return {"outputs": out}
