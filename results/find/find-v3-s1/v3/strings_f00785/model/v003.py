def predict(probe):
    # First char: letter shifted +1 (a->b, Z->A); non-letter unchanged [E1, E2]
    # Everything after first char: unchanged [E1, E2, E3]
    # Append 'y' to the whole result [E1, E2, E3]
    # Exception: if the string is exactly "x y", output "y y" (not "y yy") [E4]
    #   -> i.e. when first char is 'x' and rest is " y", the appended y replaces?
    #   Actually observed "x y" -> "y y": shift x->y, rest " y", then append y would give "y yy".
    #   Observed "y y". So the trailing space + appended y collapses? Let's check "trailing " -> "urailing y"
    #   (space kept, then y appended). And "test case " -> "uest case y" (space kept, y appended).
    #   So "x y" is special: maybe the rule is the last char is replaced by 'y' if it's a space?
    #   But "test case " -> "uest case y" keeps the space. Hmm.
    #   Wait: "test case " has trailing space, output "uest case y" = shift + "est case " + "y"? 
    #   That's "uest case " + "y" = "uest case y". Yes space kept.
    #   "x y": shift x->y, rest " y", append y -> "y yy". Observed "y y".
    #   Difference: maybe when the string ends in a single space and the char before is a letter?
    #   "test case " ends in space too. Both end in space. So why different?
    #   Let's recount: "x y" is x, space, y. Output "y y" = y, space, y. So the last 'y' is the original y? 
    #   No—shift first char x->y gives "y y", then append y would be "y yy". Observed "y y".
    #   Perhaps the rule: append 'y' only if the string doesn't already end in 'y'? 
    #   Check "test case Zebra" -> "uest case Zebray" ends in 'a' -> append y. ok.
    #   "Mississippi Hello World data" -> "...datay" append y. ok.
    #   "a b c" -> "b b cy" append y (ends c). ok.
    #   "x y" ends in 'y' -> don't append. That fits!
    #   Check E2: "a" -> "by" (ends a, append). "Z"->"Ay". "1"->"1y". "!"->"!y". " "->" y". 
    #   "ab"->"bby". "a b"->"b by". "A1!"->"B1!y". "hello world"->"iello worldy". "  "->"  y".
    #   None end in y. ok.
    #   E3: "level123"->"mevel123y". "Python!@#"->"Qython!@#y". "banana"->"cananay". 
    #   "racecar Zebra level"->"sacecar Zebra levely". "racecar"->"sacecary". "test case  "->"uest case  y".
    #   None end in y. ok.
    #   E4: "hello world"->"iello worldy". "hello  world"->"iello  worldy". " hello"->" helloy".
    #   "hello hello"->"iello helloy". "a b c"->"b b cy". "x y"->"y y" (ends y, no append). 
    #   "ab cd"->"bb cdy". "one two three"->"pne two threey". "  leading"->"  leadingy". 
    #   "trailing "->"urailing y". All consistent with: append 'y' unless result already ends in 'y'.
    #   But wait—does "already ends in y" refer to the shifted string or original? 
    #   "x y" original ends in y, shifted first char gives "y y" also ends in y. Same.
    #   Need a case where shift makes it end in y: e.g. "ax" -> shift a->b gives "bx", ends x, append -> "bxy". 
    #   Or "x" -> "y", ends y, so no append -> "y"? But E2 "a"->"by" (a->b, append y). 
    #   Hmm "x" alone: shift x->y, ends in y, would give "y" not "yy". Unknown. Mark with ?.
    #   Safer: rule is append 'y' unless the ORIGINAL string ends in 'y'? "x y" ends in y -> no append.
    #   But then "y" alone -> shift y->z, ends y original, no append -> "z". Unknown.
    #   Let's go with: append 'y' unless the shifted result already ends in 'y'.
    def shift(c):
        if 'a' <= c <= 'z':
            return chr((ord(c)-97+1)%26+97)
        if 'A' <= c <= 'Z':
            return chr((ord(c)-65+1)%26+65)
        return c
    out = []
    for s in probe["inputs"]:
        if not s:
            out.append("y")
            continue
        r = shift(s[0]) + s[1:]
        if not r.endswith("y"):
            r += "y"
        out.append(r)
    return {"outputs": out}
