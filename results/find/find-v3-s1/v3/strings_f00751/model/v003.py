def predict(probe):
    # Rule: insert "i" after the first vowel in each word [E1-E5]
    # A word = maximal run of non-space characters; spaces preserved.
    # Only the FIRST vowel of each word gets an "i" after it [E2: "banana"->"baniana", "Mississippi"->"Missiissippi"]
    # Vowels are a,e,i,o,u (lowercase) [E2: "a e i o u"->"a e ii o u" - only "i" gets one]
    # Case: only lowercase vowels count [E2: "MiXeD"->"MiXeDi" - the 'i' in MiXeD is lowercase]
    #   Wait: "MiXeD" -> "MiXeDi": first lowercase vowel is 'i' at index 1. Yes.
    #   "Python!@#" -> "Pythion!@#": first lowercase vowel 'o'. Yes.
    #   "Example" -> "Exaimple": first lowercase vowel 'a'. Yes.
    #   "Mississippi" -> "Missiissippi": first lowercase vowel 'i' at index 1. Yes.
    #   "test case " -> "test icase": word "test" first vowel 'e' -> "teist"? but observed "test icase"...
    #   Hmm: "test" -> no i inserted in "test icase". Let me recheck.
    #   E2 "test case" -> "testi case": word "test" -> "testi", first vowel 'e' at index 1 -> "teist"? No, observed "testi".
    #   So it's not "after first vowel". Let me reconsider.
    #
    # Re-examine: "test" -> "testi" (i appended at end). "case" -> "case" (unchanged in "test case").
    #   E2 "test case" -> "testi case": only "test" changed, i at end.
    #   E3 "test case  " -> "test icase": "test"->"test", "case"->"case" with i before? "test icase" = "test " + "icase".
    #   Hmm inconsistent. Let me look again.
    #
    # E1: "test case " -> "test icase" : "test " + "icase". So "case"->"icase" (i prepended).
    # E1: "test caseMiXeD" -> "test caiseMiXeD": "case"->"caise" (i after 'a').
    # E1: "test case Zebra" -> "test caise Zebra": "case"->"caise".
    # E3: "test case  " -> "test icase": "case"->"icase".
    # E2: "test case" -> "testi case": "test"->"testi".
    #
    # This is confusing. Let me think of it as: insert "i" at position len//2 of the whole string? 
    # E1 "apple" -> "apiple": len 5, mid 2 -> "ap"+"i"+"ple" = "apiple". YES.
    # E1 "test case " -> len 10, mid 5 -> "test "+"i"+"case " = "test icase ". Observed "test icase". YES (trailing space maybe stripped? or kept).
    # E1 "test caseMiXeD" -> len 14, mid 7 -> "test ca"+"i"+"seMiXeD" = "test caiseMiXeD". YES!
    # E1 "data a Python " -> len 14, mid 7 -> "data a "+"i"+"Python " = "data a iPython ". YES.
    # E1 "test case Zebra" -> len 15, mid 7 -> "test ca"+"i"+"se Zebra" = "test caise Zebra". YES.
    # E1 "Mississippi Hello World data" -> len 28, mid 14 -> "Mississippi He"+"i"+"llo World data" = "Mississippi Heillo World data". YES!
    #
    # So it IS mid insertion! The current model v2 was right. Let me check E2.
    # E2 "cat" len 3 mid 1 -> "c"+"i"+"at" = "ciat". YES.
    # "dog" -> "diog". YES. "banana" len 6 mid 3 -> "ban"+"i"+"ana" = "baniana". YES.
    # "hello world" len 11 mid 5 -> "hello"+"i"+" world" = "helloi world". YES.
    # "MiXeD case" len 10 mid 5 -> "MiXeD"+"i"+" case" = "MiXeDi case". YES.
    # "a e i o u" len 9 mid 4 -> "a e "+"i"+"i o u" = "a e ii o u". YES.
    # "123 abc" len 7 mid 3 -> "123"+"i"+" abc" = "123i abc". YES.
    # "Mississippi" len 11 mid 5 -> "Missi"+"i"+"ssippi" = "Missiissippi". YES.
    # "test case" len 9 mid 4 -> "test"+"i"+" case" = "testi case". YES.
    # "data" len 4 mid 2 -> "da"+"i"+"ta" = "daita". YES.
    #
    # E3 "level123" len 8 mid 4 -> "leve"+"i"+"l123" = "leveil123". YES.
    # "Python!@#" len 9 mid 4 -> "Pyth"+"i"+"on!@#" = "Pythion!@#". YES.
    # "banana" -> "baniana". YES.
    # "racecar Zebra level" len 19 mid 9 -> "racecar Z"+"i"+"ebra level" = "racecar Ziebra level". YES.
    # "racecar" len 7 mid 3 -> "rac"+"i"+"ecar" = "raciecar". YES.
    # "test case  " len 11 mid 5 -> "test "+"i"+"case  " = "test icase  ". Observed "test icase". Hmm trailing spaces.
    #
    # E4 "level" len 5 mid 2 -> "le"+"i"+"vel" = "leivel". YES.
    # "lemon" -> "le"+"i"+"mon" = "leimon". YES.
    # "lever" -> "leiver". YES. "seven" -> "seiven". YES.
    # "even" len 4 mid 2 -> "ev"+"i"+"en" = "evien". YES.
    # "open" -> "op"+"i"+"en" = "opien". YES.
    # "item" -> "it"+"i"+"em" = "itiem". YES.
    # "until" len 5 mid 2 -> "un"+"i"+"til" = "unitil". YES.
    # "atom" -> "at"+"i"+"om" = "atiom". YES.
    # "evil" -> "ev"+"i"+"il" = "eviil". YES.
    #
    # E5 " racecar" len 8 mid 4 -> " rac"+"i"+"ecar" = " raciecar". Observed "raciecar" (leading space gone).
    # "Mississippi" -> "Missiissippi". YES.
    # "function" len 8 mid 4 -> "func"+"i"+"tion" = "funcition". YES.
    # "racecar " len 8 mid 4 -> "race"+"i"+"car " = "raceicar ". Observed "raceicar" (trailing space gone).
    # "test case racecar" len 17 mid 8 -> "test cas"+"i"+"e racecar" = "test casie racecar". YES.
    # "Example" len 7 mid 3 -> "Exa"+"i"+"mple" = "Exaimple". YES.
    #
    # So the rule is: insert "i" at index len(s)//2, BUT leading/trailing whitespace is stripped first?
    # E5 " racecar" -> "raciecar": if we strip to "racecar" (len 7, mid 3) -> "rac"+"i"+"ecar" = "raciecar". YES.
    # E5 "racecar " -> strip to "racecar" -> "raciecar". Observed "raceicar". Hmm that's different!
    #   "racecar " -> "raceicar": if strip -> "racecar" -> "raciecar" not "raceicar".
    #   If no strip: len 8 mid 4 -> "race"+"i"+"car " = "raceicar ". Observed "raceicar" (trailing space removed).
    #   So: insert at len//2 of original, then strip trailing? But " racecar" -> " raciecar" then strip leading -> "raciecar". YES.
    # E3 "test case  " len 11 mid 5 -> "test icase  " -> strip trailing -> "test icase". YES.
    # E1 "test case " len 10 mid 5 -> "test icase " -> strip trailing -> "test icase". YES.
    # E1 "data a Python " len 14 mid 7 -> "data a iPython " -> strip -> "data a iPython". YES.
    #
    # So: insert "i" at len(s)//2, then strip leading/trailing whitespace from result.
    # Check E2 "hello world" no leading/trailing space, fine.
    #
    # But wait, does stripping happen before or after? " racecar" -> if strip first: "racecar" len 7 mid 3 -> "raciecar". Same result.
    # "racecar " -> strip first: "racecar" -> "raciecar". But observed "raceicar". So strip must be AFTER insertion.
    # Actually "racecar " len 8 mid 4 -> "race"+"i"+"car " = "raceicar " -> strip -> "raceicar". YES.
    # " racecar" len 8 mid 4 -> " rac"+"i"+"ecar" = " raciecar" -> strip -> "raciecar". YES.
    #
    # Great, consistent: insert at len//2, then .strip().
    outputs = []
    for s in probe["inputs"]:
        mid = len(s) // 2
        outputs.append((s[:mid] + "i" + s[mid:]).strip())
    return {"outputs": outputs}
