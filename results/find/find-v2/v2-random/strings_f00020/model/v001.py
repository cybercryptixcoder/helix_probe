def predict(probe):
    # Observations from E1:
    # - "abc123" -> "abc51233": a '5' inserted after "abc" (before "123")
    # - "level" -> "lev5ell": '5' inserted after "lev"
    # - " Zebralower" -> " Zebra5lowerr": '5' inserted after " Zebra", and trailing 'r' doubled
    # - "Hello World function lazy" -> "Hello World f5unction lazyy": '5' after "f", trailing 'y' doubled
    # - "bananaUPPER" -> "banana5UPPERR": '5' after "banana", trailing 'R' doubled
    # - "Zebra" -> "Zeb5raa": '5' after "Zeb", trailing 'a' doubled
    #
    # Hypothesis: insert '5' at the midpoint (len//2), and duplicate the last character.
    # Check: "abc123" len 6 -> mid 3 -> "abc"+"5"+"123" = "abc5123", then double last '3' -> "abc51233" ✓
    # "level" len 5 -> mid 2 -> "le"+"5"+"vel" = "le5vel", double 'l' -> "le5vell" ✗ (observed "lev5ell")
    # So midpoint is not len//2. Try ceil(len/2): "level" 5 -> 3 -> "lev"+"5"+"el" = "lev5el", double 'l' -> "lev5ell" ✓
    # "abc123" 6 -> 3 -> "abc5 123" -> "abc51233" ✓
    # " Zebralower" len 12 -> 6 -> " Zebra"+"5"+"lower" = " Zebra5lower", double 'r' -> " Zebra5lowerr" ✓
    # "Hello World function lazy" len 26 -> 13 -> "Hello World f"+"5"+"unction lazy", double 'y' -> "...lazyy" ✓
    # "bananaUPPER" len 11 -> 6 -> "banana"+"5"+"UPPER", double 'R' -> "banana5UPPERR" ✓
    # "Zebra" len 5 -> 3 -> "Zeb"+"5"+"ra", double 'a' -> "Zeb5raa" ✓
    #
    # Rule: insert '5' at index ceil(len/2) = (len+1)//2, then duplicate the final character.
    def transform(s):
        if not s:
            return s
        mid = (len(s) + 1) // 2
        t = s[:mid] + "5" + s[mid:]
        return t + t[-1]

    try:
        return {"outputs": [transform(x) for x in probe["inputs"]]}
    except Exception:
        return {"outputs": []}
