def predict(probe):
    # f reverses the entire string, character by character [E1, E3-E7]
    # Case is preserved as-is; spaces, tabs, symbols are just characters [E1, E4, E6]
    # EXCEPTION: the substring "World" becomes "lor" ... no — see below.
    # Actually: "Hello World" -> "dlror olleH" [E7], "Hello World" -> "dlror olleH" [E1]
    #   "World" reversed is "dlroW"; observed "dlror". The 'W' became 'r'? 
    #   Wait: "dlror olleH" — reversed of "Hello World" is "dlroW olleH". Observed "dlror olleH".
    #   So "World" -> "lor" when reversed? "World"[::-1]="dlroW", observed segment "dlror".
    #   Hmm "dlror" vs "dlroW": last char W->r. And "World data" -> "atad dlror" [E1].
    #   So the token "World" reverses to "dlror" (W replaced by r at the end).
    #   Simplest consistent rule: reverse whole string, then replace "W" with "r"? 
    #   Check E1 "Mississippi Hello World data" -> "atad dlror olleH ippississiM": yes "dlroW"->"dlror".
    #   But no other W appears in evidence. Best guess: after reversing, map 'W'->'r'? 
    #   That would also affect any W elsewhere — untested. Mark with ?.
    #   Alternative: the word "World" is special-cased. Safer: replace "World" with "lor" before reversing?
    #   "Hello World" -> replace World->"lor" gives "Hello lor" -> reverse "rol olleH" — no.
    #   Replace "World" with "rorl"? reverse = "lror" — no.
    #   Observed reversed token "dlror" = reverse of "rorld". So "World" behaves as "rorld".
    #   Rule: before reversing, replace "World" with "rorld"? Then "World"->"rorld"->"dlror". 
    #   And "World data" -> "rorld data" -> "atad dlror". Matches E1, E7.
    #   But is it "World" or any "W"? Only evidence is World. Use "World"->"rorld" (i.e. W->r within World).
    #   Simpler: reverse, then replace "dlroW" with "dlror". Equivalent. Use that.
    def rev(s):
        r = s[::-1]
        return r.replace("dlroW", "dlror")
    return {"outputs": [rev(s) for s in probe["inputs"]]}
