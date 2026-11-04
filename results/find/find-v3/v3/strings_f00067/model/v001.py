def predict(probe):
    # Hypothesis: f reverses the string, then applies a Caesar-like shift
    # to letters that depends on position? Let's check evidence.
    # E1:
    # "abc123" -> "3321cba" : reverse is "321cba", but got "3321cba"
    #   reverse("abc123") = "321cba". Observed "3321cba" = "3"+"321cba"? 
    #   Actually "3321cba": reverse gives "321cba"; observed has extra leading 3.
    #   Hmm: "abc123" reversed = "321cba". Observed "3321cba". 
    #   Maybe digits shifted? '1'->'3'? '2'->'3'? no.
    # "level" -> "llevel": reverse("level")="level", observed "llevel" = "l"+"level"
    # " Zebralower" -> "rrewolarbeZ": reverse(" Zebralower")="rewolarbeZ " 
    #   observed "rrewolarbeZ" = "r"+"rewolarbeZ" (space dropped, extra r prepended)
    # "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal"
    #   reverse = "yzal noitcnuf dlroW olleH"
    #   observed = "olleH dlroW noitcnuf yyzal"
    #   That's reverse of words order? Let's see: words: Hello World function lazy
    #   reversed words order: lazy function World Hello
    #   each word reversed: yzal noitcnuf dlroW olleH
    #   observed: "olleH dlroW noitcnuf yyzal" -> Hello World function lazy reversed per word? 
    #   "olleH"=reverse(Hello), "dlroW"=reverse(World), "noitcnuf"=reverse(function), "yyzal"=reverse(lazy) but with extra y: "yzal"->"yyzal"
    #   So words kept in order, each reversed, but "lazy"->"yyzal" has extra y.
    # "bananaUPPER" -> "RREPPUananab": reverse = "RREPPUananab" exactly! 
    #   reverse("bananaUPPER") = "RREPPUananab". Yes matches.
    # "Zebra" -> "aarbeZ": reverse = "arbeZ", observed "aarbeZ" extra a.
    #
    # Pattern: mostly reverse. But sometimes an extra character inserted.
    # "abc123"->"3321cba": reverse="321cba", extra '3' at front.
    # "level"->"llevel": reverse="level", extra 'l' at front.
    # " Zebralower"->"rrewolarbeZ": reverse="rewolarbeZ ", observed "rrewolarbeZ" 
    #    = reverse with trailing space removed, extra 'r' at front.
    # "Hello World function lazy"->"olleH dlroW noitcnuf yyzal":
    #    reverse whole = "yzal noitcnuf dlroW olleH". Observed is different word order.
    #    Wait observed: "olleH dlroW noitcnuf yyzal" - words in original order, each reversed.
    #    Hmm but "bananaUPPER" single word reversed whole = same as word reversed.
    #    "Zebra" single word.
    #    So maybe: reverse each word, keep word order? Check "abc123": single token, reverse="321cba", observed "3321cba" extra 3.
    #    "level": reverse="level", observed "llevel" extra l.
    #    " Zebralower": single token (leading space), reverse="rewolarbeZ ", observed "rrewolarbeZ" - space removed, extra r.
    #    "Hello World function lazy": words reversed individually, order kept: 
    #       Hello->olleH, World->dlroW, function->noitcnuf, lazy->yzal but observed yyzal (extra y).
    #    "bananaUPPER"->"RREPPUananab" = reverse, no extra.
    #    "Zebra"->"aarbeZ": reverse="arbeZ", extra a.
    #
    # Extra character: seems to duplicate the first character of the reversed string?
    #   "321cba" -> "3"+"321cba" = "3321cba" yes
    #   "level" -> "l"+"level" = "llevel" yes
    #   "rewolarbeZ " -> first char 'r', but also space removed. "r"+"rewolarbeZ" = "rrewolarbeZ" yes (space stripped)
    #   "yzal" -> "y"+"yzal" = "yyzal" yes
    #   "RREPPUananab" -> first char 'R', would give "RRREPPUananab" but observed "RREPPUananab" no extra!
    #   "arbeZ" -> first char 'a', "a"+"arbeZ"="aarbeZ" yes
    #
    # So bananaUPPER is exception? Or rule depends on something.
    # bananaUPPER: has uppercase in middle. Maybe if string has uppercase, no duplication?
    # Zebra: has uppercase Z but duplication happened.
    # Hmm.
    # Maybe duplication happens only if first char of reversed (last char of original) is lowercase?
    #   abc123 last char '3' digit -> duplicated '3'. 
    #   level last 'l' lowercase -> dup.
    #   " Zebralower" last 'r' lowercase -> dup.
    #   lazy last 'y' lowercase -> dup.
    #   bananaUPPER last 'R' uppercase -> no dup!
    #   Zebra last 'a' lowercase -> dup.
    # That fits! Rule: reverse, then if last char of original (first of reversed) is lowercase letter, prepend it again.
    # But wait "abc123" last char '3' is digit, not lowercase letter, yet duplicated.
    # So maybe: duplicate unless last char is uppercase letter.
    #   '3' not uppercase -> dup. 'l' not uppercase -> dup. 'r' -> dup. 'y' -> dup. 'R' uppercase -> no dup. 'a' -> dup.
    # Fits all!
    #
    # Also space handling: " Zebralower" -> space removed. Maybe spaces stripped? 
    #   "Hello World function lazy" spaces kept between words.
    #   Leading space removed. Maybe strip whitespace before processing?
    #   " Zebralower".strip() = "Zebralower", reverse="rewolarbeZ", last char 'r' lowercase -> dup -> "rrewolarbeZ". Matches!
    #
    # But "Hello World function lazy": strip then reverse whole = "yzal noitcnuf dlroW olleH", 
    #   last char 'H' uppercase -> no dup. But observed is word-by-word reversed!
    #   So multi-word: reverse each word, keep order, join with space.
    #   Check: "Hello World function lazy" -> "olleH dlroW noitcnuf yzal", 
    #   then dup rule on whole? last char of original 'y' lowercase -> prepend 'y'? 
    #   But observed "yyzal" has extra y at start of last word, not whole string.
    #   Hmm. Actually observed "olleH dlroW noitcnuf yyzal": extra y prepended to last word's reversed form.
    #   So maybe rule applies per word? Each word reversed, then dup first char of reversed if last char of word not uppercase?
    #   Hello: last 'o' lowercase -> "o"+"olleH"="oolleH"? but observed "olleH". No.
    #   Hmm inconsistent.
    #
    # Let me reconsider. Maybe it's not word-by-word. 
    # "Hello World function lazy" observed "olleH dlroW noitcnuf yyzal"
    # Reverse whole string: "yzal noitcnuf dlroW olleH"
    # Observed is reverse of that? No.
    # Observed words: olleH dlroW noitcnuf yyzal
    # That's each word reversed, in original order, with last word getting extra y.
    # Maybe: reverse each word, then apply dup rule to the LAST word only? 
    #   last word "lazy" reversed "yzal", last char of original word 'y' lowercase -> dup -> "yyzal". Others no dup.
    # But single-word cases: dup applied. 
    # Maybe dup applies to last word (or whole if single word).
    #   "abc123" single word -> dup '3' -> "3321cba" yes
    #   "level" -> "llevel" yes
    #   " Zebralower" -> strip, single word "Zebralower" -> "rrewolarbeZ" yes
    #   "bananaUPPER" -> last char 'R' uppercase -> no dup -> "RREPPUananab" yes
    #   "Zebra" -> 'a' lowercase -> dup -> "aarbeZ" yes
    #   "Hello World function lazy" -> last word lazy -> "yzal" dup -> "yyzal", others plain reversed. Matches!
    #
    # So model: split into words (on spaces), reverse each word, keep order, join with single space.
    # Then on the last word's reversed form, if the last character of the original last word is not uppercase, prepend that char.
    # Wait but for single word, last word = whole.
    # Also leading/trailing spaces stripped.
    # Check " Zebralower": strip -> "Zebralower", one word.
    #
    # What about multiple spaces? Unknown. Assume split on whitespace and join single space.
    # What about empty string? Unknown, guess returns "".
    #
    # Let me double check "bananaUPPER": last char 'R' uppercase -> no dup. Good.
    # What if last char is digit or symbol? "abc123" last '3' -> dup. So rule: dup unless uppercase letter.
    #
    # Edge: what if last char is space after strip? stripped.
    #
    # I'll implement: 
    #   s = input.strip()
    #   if s == "": return ""
    #   words = s.split()  # splits on any whitespace
    #   rev = [w[::-1] for w in words]
    #   last_orig = words[-1]
    #   if last_orig and not last_orig[-1].isupper():
    #       rev[-1] = last_orig[-1] + rev[-1]
    #   return " ".join(rev)
    #
    # Wait check "abc123": words=["abc123"], rev=["321cba"], last char '3' not upper -> "3"+"321cba"="3321cba" yes.
    # "level": "l"+"level"="llevel" yes.
    # " Zebralower": strip "Zebralower", rev "rewolarbeZ", 'r' -> "rrewolarbeZ" yes.
    # "Hello World function lazy": words 4, rev ["olleH","dlroW","noitcnuf","yzal"], last 'y' -> "yyzal", join -> "olleH dlroW noitcnuf yyzal" yes!
    # "bananaUPPER": rev "RREPPUananab", last 'R' upper -> no dup -> matches.
    # "Zebra": rev "arbeZ", 'a' -> "aarbeZ" yes.
    #
    # Great, fits all 6.
    def predict(probe):
        outs = []
        for s in probe.get("inputs", []):
            t = s.strip()
            if t == "":
                outs.append("")
                continue
            words = t.split()
            rev = [w[::-1] for w in words]
            last = words[-1]
            if last and not last[-1].isupper():
                rev[-1] = last[-1] + rev[-1]
            outs.append(" ".join(rev))
        return {"outputs": outs}
    return predict(probe)
