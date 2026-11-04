import re

def predict(probe):
    # Hypothesis from E1: a 'Z' is inserted into each string.
    # Observations:
    #   "abc123" -> "abcZ123"  (Z after 3 chars)
    #   "level"  -> "leZvel"   (Z after 2 chars)
    #   " Zebralower" -> "ZebraZlower" (Z after 5 chars; note leading space removed)
    #   "Hello World function lazy" -> "HelloWorldfZunctionlazy" (spaces removed, Z after 10 chars)
    #   "bananaUPPER" -> "bananZaUPPER" (Z after 5 chars)
    #   "Zebra" -> "ZeZbra" (Z after 2 chars)
    #
    # Pattern: spaces are removed first. Then a 'Z' is inserted at position
    # floor(len/2) of the space-stripped string? Let's check:
    #   abc123 len6 -> pos3 = "abc"+"Z"+"123" ✓
    #   level len5 -> pos2 = "le"+"Z"+"vel" ✓
    #   " Zebralower" -> "Zebralower" len10 -> pos5 = "Zebra"+"Z"+"lower" ✓
    #   "Hello World function lazy" -> "HelloWorldfunctionlazy" len23 -> pos? observed "HelloWorldf"+"Z"+"unctionlazy" = pos11, floor(23/2)=11 ✓
    #   bananaUPPER len11 -> pos5 = "banan"+"Z"+"aUPPER" ✓
    #   Zebra len5 -> pos2 = "Ze"+"Z"+"bra" ✓
    # So: remove spaces, insert 'Z' at floor(len/2).
    out = []
    for s in probe.get("inputs", []):
        t = s.replace(" ", "")
        k = len(t) // 2
        out.append(t[:k] + "Z" + t[k:])
    return {"outputs": out}
