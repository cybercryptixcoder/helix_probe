def predict(probe):
    # Observations from E1:
    # "abc123" -> "abc51233": a '5' inserted after position 3 (after "abc")
    # "level" -> "lev5ell": '5' inserted after position 3
    # " Zebralower" -> " Zebra5lowerr": '5' inserted after position 5? Let's check.
    #   " Zebralower" indices: 0=' ',1='Z',2='e',3='b',4='r',5='a',6='l',7='o',8='w',9='e',10='r'
    #   output " Zebra5lowerr": " Zebra" + "5" + "lower" + "r" -> inserted after index 5 ('a'), and an extra 'r' appended.
    # "Hello World function lazy" -> "Hello World f5unction lazyy": '5' inserted after "Hello World f" (index 13), extra 'y' appended.
    # "bananaUPPER" -> "banana5UPPERR": '5' inserted after "banana" (index 6), extra 'R' appended.
    # "Zebra" -> "Zeb5raa": '5' inserted after "Zeb" (index 3), extra 'a' appended.
    #
    # Pattern hypothesis: insert '5' at index = len(s)//2 (integer division).
    #   abc123 len6 -> 3: "abc"+"5"+"123" = "abc5123" but observed "abc51233" (extra char)
    #   level len5 -> 2: "le"+"5"+"vel" = "le5vel" but observed "lev5ell" (insert at 3)
    # Hmm, len//2 for level=2, but observed insert at 3. So maybe (len+1)//2?
    #   abc123 len6 -> (6+1)//2=3: "abc"+"5"+"123"="abc5123", observed "abc51233" extra '3'
    #   level len5 -> (5+1)//2=3: "lev"+"5"+"el"="lev5el", observed "lev5ell" extra 'l'
    #   " Zebralower" len11 -> (11+1)//2=6: " Zebra"+"5"+"lower"=" Zebra5lower", observed " Zebra5lowerr" extra 'r'
    #   "Hello World function lazy" len25 -> (25+1)//2=13: "Hello World f"+"5"+"unction lazy"="Hello World f5unction lazy", observed "...lazyy" extra 'y'
    #   "bananaUPPER" len11 -> 6: "banana"+"5"+"UPPER"="banana5UPPER", observed "banana5UPPERR" extra 'R'
    #   "Zebra" len5 -> 3: "Zeb"+"5"+"ra"="Zeb5ra", observed "Zeb5raa" extra 'a'
    #
    # So: insert '5' at index (len+1)//2, then append the last character of the original string.
    # Check: last char of abc123='3' -> "abc5123"+"3"="abc51233" ✓
    #   level last='l' -> "lev5el"+"l"="lev5ell" ✓
    #   " Zebralower" last='r' -> " Zebra5lower"+"r"=" Zebra5lowerr" ✓
    #   "...lazy" last='y' -> "...lazy"+"y"="...lazyy" ✓
    #   "bananaUPPER" last='R' -> "banana5UPPER"+"R"="banana5UPPERR" ✓
    #   "Zebra" last='a' -> "Zeb5ra"+"a"="Zeb5raa" ✓
    #
    # Rule: out = s[:(len+1)//2] + "5" + s[(len+1)//2:] + s[-1]
    # Edge: empty string -> ? guess return "5" (no last char). Marked with "?".
    def f(s):
        if len(s) == 0:
            return "5"  # ? unknown for empty
        k = (len(s) + 1) // 2
        return s[:k] + "5" + s[k:] + s[-1]

    return {"outputs": [f(x) for x in probe["inputs"]]}
