def predict(probe):
    # Rule: split input on whitespace into words (runs of spaces collapse, leading/trailing ignored) [E4]
    # If there are no words (empty/whitespace-only), output is "lmKA" + reversed input? [E4 "  y" -> "lmKAy"]
    # Actually: reverse the whole string, then insert "lmKA" at the position of the last space
    #   but with runs of spaces collapsed to a single space in the output [E4]
    # Evidence:
    #   "a  b" -> "a lmKAb": reverse = "b  a", last space region -> "a lmKAb" (spaces collapsed)
    #   "a   b" -> "a lmKAb"
    #   "a b " -> "a b lmKA": reverse = " b a", trailing space becomes... "a b lmKA"
    #   "a b  c" -> "a b lmKAc": reverse = "c  b a" -> "a b lmKAc"
    #   " leading" -> "lmKAgnidael"
    #   "trailing " -> "gniliart lmKA"
    #   "two  spaces  here" -> "owt secaps lmKAereh"
    #   "x  " -> "x lmKA"
    #   "  y" -> "lmKAy"
    #   "a b c " -> "a b c lmKA"
    # Mechanism: reverse the string, then collapse each run of spaces into one space,
    #   then insert "lmKA" adjacent to the (single) space that came from the last space run?
    # Simpler: reverse string, collapse spaces to single, then insert "lmKA" before the last space
    #   if there is a space, else prepend "lmKA".
    # Check "a  b": rev "b  a" -> collapse "b a" -> insert before last space: "b lmKAa"? No, observed "a lmKAb".
    # Hmm. Let's think differently.
    # Observed pattern: output = reverse(prefix) + " lmKA" + reverse(lastword), where prefix/lastword
    #   are split at the LAST space, and the space itself is replaced by " lmKA".
    #   "a  b": last space at index 2, prefix="a ", lastword="b" -> reverse("a ")=" a", so " a lmKAb"? but observed "a lmKAb".
    # So spaces in prefix get collapsed/stripped. reverse("a ") = " a" -> strip/collapse -> "a".
    #   "a   b": prefix="a  " -> reverse="  a" -> collapse -> "a". Good.
    #   "a b ": last space at index 3, prefix="a b", lastword="" -> reverse("a b")="b a", + " lmKA" + "" = "b a lmKA"? observed "a b lmKA".
    # So when lastword is empty, it's different: output = reverse(prefix) with spaces collapsed + " lmKA".
    #   reverse("a b")="b a" -> but observed "a b lmKA". So NOT reversed when lastword empty?
    #   "a b c ": prefix="a b c", observed "a b c lmKA" = prefix unchanged + " lmKA".
    #   "trailing ": prefix="trailing", observed "gniliart lmKA" = reverse(prefix) + " lmKA". Contradiction!
    # Wait "trailing " -> "gniliart lmKA": reverse("trailing")="gniliart". Yes reversed.
    # "a b " -> "a b lmKA": reverse("a b")="b a" != "a b". Hmm.
    # Unless: split on spaces into words, reverse the ORDER? No.
    # Let's reconsider: maybe it's reverse the whole string, then collapse spaces, then move "lmKA"?
    # "a b ": rev = " b a". collapse = " b a". observed "a b lmKA". 
    # "trailing ": rev = " gniliart". observed "gniliart lmKA".
    # "a b c ": rev = " c b a". observed "a b c lmKA".
    # "x  ": rev = "  x". observed "x lmKA".
    # "  y": rev = "y  ". observed "lmKAy".
    # Pattern for trailing-space cases: output = reverse(string with trailing spaces removed) + " lmKA"?
    #   "a b " -> strip -> "a b" -> reverse -> "b a"? no, observed "a b".
    # Hmm "a b" reversed is "b a". Observed "a b lmKA". So not reversed.
    # Wait maybe the rule is: reverse each WORD, keep word order? 
    #   "a b" -> "a b"? no, E2 "ab cd" -> "ba lmKAdc" (each word reversed: "ba","dc"). Yes!
    #   "a b " -> words ["a","b"] -> "a b" + " lmKA" = "a b lmKA". Yes!
    #   "a b c " -> "a b c lmKA". Yes!
    #   "trailing " -> "gniliart lmKA". Yes!
    #   "x  " -> "x lmKA". Yes!
    #   "  y" -> "lmKAy": words ["y"], no trailing space... but leading space. Hmm "lmKA"+"y".
    #   " leading" -> "lmKAgnidael": word "leading" reversed "gnidael", prepend "lmKA".
    #   "two  spaces  here" -> words ["two","spaces","here"] -> "owt secaps ereh"? observed "owt secaps lmKAereh".
    #   So "lmKA" goes before the LAST word, not at end. 
    #   "a b " -> words ["a","b"], last word "b", so "a lmKAb"? but observed "a b lmKA". 
    #   Difference: trailing space present -> "lmKA" at end.
    # Let me re-examine. Maybe: reverse whole string, collapse spaces, then if original had trailing space, move lmKA to end?
    # This is getting complex. Let me tabulate:
    #   "a  b"      -> "a lmKAb"       (no trailing sp)
    #   "a   b"     -> "a lmKAb"
    #   "a b "      -> "a b lmKA"      (trailing sp)
    #   "a b  c"    -> "a b lmKAc"
    #   " leading"  -> "lmKAgnidael"   (leading sp)
    #   "trailing " -> "gniliart lmKA" (trailing sp)
    #   "two  spaces  here" -> "owt secaps lmKAereh"
    #   "x  "       -> "x lmKA"        (trailing sp)
    #   "  y"       -> "lmKAy"         (leading sp)
    #   "a b c "    -> "a b c lmKA"    (trailing sp)
    # Hypothesis: reverse the whole string, then collapse runs of spaces to single space,
    #   then insert "lmKA" at the position of the last space in the ORIGINAL string,
    #   mapped through reversal... 
    # Let's test: reverse whole string, collapse spaces:
    #   "a  b" -> "b  a" -> "b a". observed "a lmKAb". Not matching.
    # OK new idea: the operation reverses the string, but "lmKA" is inserted at a fixed position
    #   relative to the last space in the ORIGINAL string, and spaces collapse.
    # Original "a  b": last space run at positions 1-2. After reverse+collapse: "b a". 
    #   Insert lmKA where? observed "a lmKAb" = "a" + " lmKA" + "b". 
    #   That's reverse of "a" then "lmKA" then reverse of "b". So it's: reverse each segment split by last space run.
    #   prefix "a", lastword "b": reverse(prefix)="a", reverse(lastword)="b" -> "a lmKAb". Yes!
    #   "a b ": last space run at end (position 3). prefix="a b", lastword="". 
    #     reverse(prefix)="b a", reverse(lastword)="" -> "b a lmKA"? observed "a b lmKA". No.
    # Hmm. Unless trailing space means lastword is empty and prefix is NOT reversed?
    #   "trailing ": prefix="trailing", lastword="" -> observed "gniliart lmKA" = reverse(prefix)+" lmKA". Reversed!
    #   "a b ": prefix="a b", observed "a b lmKA". Not reversed. Contradiction.
    # Unless "a b" reversed is "b a" but observed "a b". So maybe words are reversed individually, order kept?
    #   "a b" -> "a b" (each word len 1). "trailing" -> "gniliart". "a b c" -> "a b c". Yes all consistent!
    #   "two spaces here" -> "owt secaps ereh", observed "owt secaps lmKAereh" - lmKA before last word.
    #   So: reverse each word, keep order, insert "lmKA" before the last word.
    #   But "a b " -> "a b lmKA": last word is "" (empty after trailing space)? Then lmKA at end. 
    #   "trailing " -> "gniliart lmKA": last word empty -> lmKA at end. Yes!
    #   "x  " -> "x lmKA": last word empty -> lmKA at end. Yes!
    #   "a b c " -> "a b c lmKA": last word empty -> lmKA at end. Yes!
    #   "  y" -> "lmKAy": words ["","y"]? leading space. First word empty. Last word "y". 
    #     reverse each: "" and "y". Insert lmKA before last word: "lmKAy". Yes!
    #   " leading" -> "lmKAgnidael": words ["","leading"] -> "lmKAgnidael". Yes!
    #   "a  b" -> words ["a","b"] (collapse) -> "a lmKAb". Yes!
    #   "a b  c" -> words ["a","b","c"] -> "a b lmKAc". Yes!
    #   "two  spaces  here" -> ["two","spaces","here"] -> "owt secaps lmKAereh". Yes!
    #   "ab cd" -> ["ab","cd"] -> "ba lmKAdc". Yes!
    #   "x y z" -> ["x","y","z"] -> "x y lmKAz". Yes!
    #   "one two three" -> ["one","two","three"] -> "eno owt lmKAeerht". Yes!
    #   "A B C D" -> ["A","B","C","D"] -> "A B C lmKAD". Yes!
    #   "test case" -> ["test","case"] -> "tset lmKAesac". Yes!
    #   "banana data banana " -> ["banana","data","banana",""] -> "ananab atad ananab lmKA". Yes!
    #   "Hello World function lazy" -> ["Hello","World","function","lazy"] -> "olleH dlroW noitcnuf lmKAyzal". Yes!
    #   No-space cases: "abc123" -> ["abc123"] -> "lmKA321cba". Yes! (single word, lmKA prepended)
    #   "level" -> "lmKAlevel". Yes!
    #   " Zebralower" -> ["","Zebralower"] -> "lmKArewolarbeZ". Yes!
    #   "bananaUPPER" -> "lmKAREPPUananab". Yes!
    #   "Zebra" -> "lmKAarbeZ". Yes!
    #   "Example123" -> "lmKA321elpmaxE". Yes!
    #   "lazy" -> "lmKAyzal". Yes!
    #   "banana" -> "lmKAananab". Yes!
    #   "level" -> "lmKAlevel". Yes!
    # So the rule: split on single spaces (preserving empty strings from leading/trailing/multiple spaces? 
    #   No - "a  b" -> "a lmKAb" means multiple spaces collapse to one separator, no empty word between).
    #   But "  y" -> "lmKAy" means leading spaces produce ONE empty first word (not two).
    #   And "x  " -> "x lmKA" means trailing spaces produce ONE empty last word.
    #   So: split on runs of spaces (re.split on ' +'), which gives empty strings at start/end if 
    #   string starts/ends with space. "a  b".split() would give ["a","b"] (no empties). 
    #   re.split(' +', "a  b") = ["a","b"]. re.split(' +', "  y") = ["","y"]. 
    #   re.split(' +', "x  ") = ["x",""]. re.split(' +', "a b ") = ["a","b",""]. 
    #   re.split(' +', "a  b") = ["a","b"]. Good.
    #   re.split(' +', "a   b") = ["a","b"]. Good.
    #   re.split(' +', "two  spaces  here") = ["two","spaces","here"]. Good.
    #   re.split(' +', " leading") = ["","leading"]. Good.
    #   re.split(' +', "trailing ") = ["trailing",""]. Good.
    #   re.split(' +', "a b  c") = ["a","b","c"]. Good.
    #   re.split(' +', "a b c ") = ["a","b","c",""]. Good.
    #   re.split(' +', "abc123") = ["abc123"]. Good.
    # Then: reverse each word, join with " ", and insert "lmKA" before the last word.
    #   If only one word: "lmKA" + reversed(word).
    #   If multiple: join reversed words[:-1] with " ", then " lmKA" + reversed(words[-1]).
    # Wait "a b " -> words ["a","b",""], reversed: ["a","b",""], join[:-1]="a b", + " lmKA" + "" = "a b lmKA". Yes!
    # "  y" -> ["","y"] -> reversed ["","y"], join[:-1]="" , + " lmKA" + "y" = " lmKAy". 
    #   But observed "lmKAy" (no leading space). So empty first word contributes nothing / no leading space.
    # Hmm. "a b " -> "a b lmKA" has space before lmKA. "  y" -> "lmKAy" no space before lmKA.
    # Difference: in "a b ", the empty is LAST word; in "  y", empty is FIRST word.
    # Maybe: join non-empty reversed words with " ", then handle lmKA placement.
    # Let me reconsider: maybe it's just reverse the whole string, then collapse spaces, then 
    #   insert lmKA at the position corresponding to the last space in original.
    #   "  y": rev = "y  " -> collapse "y " -> strip? "y". Insert lmKA at... 
    # This is getting too deep. Let me just go with: reverse each word, join with single space,
    #   strip leading/trailing spaces, then insert "lmKA" before the last word (or prepend if one word).
    #   "a b " -> words ["a","b",""], reversed ["a","b",""], join "a b " -> strip "a b" -> insert before last "a lmKAb"? 
    #   But observed "a b lmKA". So trailing empty word matters: lmKA goes at end.
    # OK: keep empty words but when joining, empty words produce no extra space issue:
    #   Actually let's just do: reversed_words = [w[::-1] for w in words]
    #   result = " ".join(reversed_words[:-1]) + " lmKA" + reversed_words[-1]
    #   then strip leading space if it starts with " lmKA" (i.e., first part empty).
    #   "  y": words ["","y"], rev ["","y"], join[:-1]="" + " lmKA" + "y" = " lmKAy" -> strip leading -> "lmKAy". Yes!
    #   "a b ": words ["a","b",""], rev ["a","b",""], join[:-1]="a b" + " lmKA" + "" = "a b lmKA". Yes!
    #   " leading": words ["","leading"], rev ["","gnidael"], "" + " lmKA" + "gnidael" = " lmKAgnidael" -> strip -> "lmKAgnidael". Yes!
    #   "trailing ": words ["trailing",""], rev ["gniliart",""], "gniliart" + " lmKA" + "" = "gniliart lmKA". Yes!
    #   "x  ": words ["x",""], rev ["x",""], "x" + " lmKA" + "" = "x lmKA". Yes!
    #   "a  b": words ["a","b"], rev ["a","b"], "a" + " lmKA" + "b" = "a lmKAb". Yes!
    #   "a b  c": words ["a","b","c"], rev ["a","b","c"], "a b" + " lmKA" + "c" = "a b lmKAc". Yes!
    #   "two  spaces  here": ["two","spaces","here"], rev ["owt","secaps","ereh"], "owt secaps"+" lmKA"+"ereh" = "owt secaps lmKAereh". Yes!
    #   "abc123": ["abc123"], rev ["321cba"], join[:-1]="" + " lmKA" + "321cba" = " lmKA321cba" -> strip -> "lmKA321cba". Yes!
    #   "level": "lmKAlevel". Yes!
    #   " Zebralower": ["","Zebralower"], rev ["","rewolarbeZ"], ""+" lmKA"+"rewolarbeZ" = " lmKArewolarbeZ" -> strip -> "lmKArewolarbeZ". Yes!
    #   "bananaUPPER": "lmKAREPPUananab". Yes!
    #   "Zebra": "lmKAarbeZ". Yes!
    #   "Example123": "lmKA321elpmaxE". Yes!
    #   "test case": ["test","case"], rev ["tset","esac"], "tset"+" lmKA"+"esac" = "tset lmKAesac". Yes!
    #   "banana data banana ": ["banana","data","banana",""], rev ["ananab","atad","ananab",""], "ananab atad ananab"+" lmKA"+"" = "ananab atad ananab lmKA". Yes!
    #   "lazy": "lmKAyzal". Yes!
    #   "banana": "lmKAananab". Yes!
    #   "Hello World function lazy": ["Hello","World","function","lazy"], rev ["olleH","dlroW","noitcnuf","yzal"], "olleH dlroW noitcnuf"+" lmKA"+"yzal" = "olleH dlroW noitcnuf lmKAyzal". Yes!
    #   "ab cd": ["ab","cd"], rev ["ba","dc"], "ba"+" lmKA"+"dc" = "ba lmKAdc". Yes!
    #   "x y z": ["x","y","z"], rev ["x","y","z"], "x y"+" lmKA"+"z" = "x y lmKAz". Yes!
    #   "one two three": ["one","two","three"], rev ["eno","owt","eerht"], "eno owt"+" lmKA"+"eerht" = "eno owt lmKAeerht". Yes!
    #   "A B C D": ["A","B","C","D"], rev same, "A B C"+" lmKA"+"D" = "A B C lmKAD". Yes!
    #   "a b": ["a","b"], rev ["a","b"], "a"+" lmKA"+"b" = "a lmKAb". Yes!
    # All match! 
    import re
    out = []
    for s in probe.get("inputs", []):
        if s == "":
            out.append("lmKA")
            continue
        words = re.split(r' +', s)
        rev = [w[::-1] for w in words]
        res = " ".join(rev[:-1]) + " lmKA" + rev[-1]
        if res.startswith(" "):
            res = res[1:]
        out.append(res)
    return {"outputs": out}
