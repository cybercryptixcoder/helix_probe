def predict(probe):
    # Insert "5" at the midpoint (index len//2) and duplicate the last character [E1, E2]
    #   "cat" (3) -> "ca"+"5"+"t"+"t" = "ca5tt" ✓
    #   "abc123" (6) -> "abc"+"5"+"123"+"3" = "abc51233" ✓
    #   "level" (5) -> "le"+"5"+"vel"+"l" = "le5vell" ... but observed "lev5ell"
    # Hmm: "level" observed "lev5ell" -> insert after index 3 (len//2+1?) 
    # Recheck: "level" len 5, "lev5ell" = "lev"+"5"+"ell" -> after 3 chars = ceil(len/2)
    #   "cat" len 3 -> ceil(3/2)=2 -> "ca"+"5"+"t"+"t" = "ca5tt" ✓
    #   "abc123" len 6 -> ceil(6/2)=3 -> "abc"+"5"+"123"+"3" ✓
    #   "Zebra" len 5 -> ceil=3 -> "Zeb"+"5"+"ra"+"a" = "Zeb5raa" ✓
    #   "bananaUPPER" len 11 -> ceil=6 -> "banana"+"5"+"UPPER"+"R" = "banana5UPPERR" ✓
    #   "Hello World function lazy" len 25 -> ceil=13 -> "Hello World f"+"5"+"unction lazy"+"y" ✓
    #   " Zebralower" len 11 -> ceil=6 -> " Zebra"+"5"+"lower"+"r" ✓
    #   "monkey" len 6 -> ceil=3 -> "mon"+"5"+"key"+"y" = "mon5keyy" ✓
    #   "ocean" len 5 -> ceil=3 -> "oce"+"5"+"an"+"n" = "oce5ann" ✓
    # So: insert at index ceil(len/2) = (len+1)//2, then append last char.
    outs = []
    for s in probe.get("inputs", []):
        if len(s) == 0:
            outs.append("5")
        else:
            k = (len(s) + 1) // 2
            outs.append(s[:k] + "5" + s[k:] + s[-1])
    return {"outputs": outs}
