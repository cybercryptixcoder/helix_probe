def predict(probe):
    # Observations from E1:
    # "abc123" -> "3321cba": reverse the string, then map digits? 
    #   reverse("abc123") = "321cba", but output is "3321cba".
    #   Hmm. Let's look closer.
    # "level" -> "llevel": prepend 'l'? Or reverse? reverse("level")="level" (palindrome).
    #   Output "llevel" = 'l' + "level". So maybe first char duplicated at front?
    # " Zebralower" -> "rrewolarbeZ": reverse(" Zebralower") = "rewolarbeZ " (trailing space).
    #   Output "rrewolarbeZ" = 'r' + "ewolarbeZ"? Actually reverse is "rewolarbeZ ".
    #   Output starts "rr..." so first char 'r' duplicated, and trailing space dropped?
    # "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal"
    #   reverse = "yzal noitcnuf dlroW olleH". Output = "olleH dlroW noitcnuf yyzal".
    #   That's reverse of words order? No. Let's see: output words: olleH dlroW noitcnuf yyzal.
    #   Input words: Hello World function lazy. Each word reversed: olleH dlroW noitcnuf yzal.
    #   Output last word "yyzal" = 'y' + "yzal"? Wait "lazy" reversed = "yzal", output "yyzal" = 'y'+'yzal'.
    #   So each word reversed, and the first letter of each word duplicated at front of that word?
    #   Check "Hello" reversed "olleH", output "olleH" — no duplication? Hmm.
    #   Wait maybe it's: reverse whole string, then duplicate first char of result?
    #   reverse("Hello World function lazy") = "yzal noitcnuf dlroW olleH".
    #   Output = "olleH dlroW noitcnuf yyzal". That's not it.
    # Let's reconsider: maybe reverse each word, keep word order? 
    #   "Hello"->"olleH", "World"->"dlroW", "function"->"noitcnuf", "lazy"->"yzal".
    #   Joined: "olleH dlroW noitcnuf yzal". Output: "olleH dlroW noitcnuf yyzal".
    #   Difference: "yyzal" vs "yzal" — extra 'y' at start.
    # "bananaUPPER" -> "RREPPUananab": reverse = "RREPPUananab". Exact reverse!
    # "Zebra" -> "aarbeZ": reverse = "arbeZ". Output "aarbeZ" = 'a'+"arbeZ". Extra 'a'.
    # "abc123" -> reverse = "321cba". Output "3321cba" = '3'+"321cba". Extra '3'.
    # "level" -> reverse = "level". Output "llevel" = 'l'+"level". Extra 'l'.
    # " Zebralower" -> reverse = "rewolarbeZ ". Output "rrewolarbeZ". 
    #   reverse without trailing space? "rewolarbeZ". Output 'r'+"ewolarbeZ"? 
    #   Hmm reverse of " Zebralower" = "rewolarbeZ " (with space at end). Strip? "rewolarbeZ".
    #   Output "rrewolarbeZ" = 'r' + "ewolarbeZ". That's 'r' + reverse[1:]? reverse="rewolarbeZ", reverse[1:]="ewolarbeZ". Yes!
    #   So output = first char of reverse + reverse? = 'r'+"rewolarbeZ" = "rrewolarbeZ". Yes!
    # Check "abc123": reverse="321cba", first char '3', output '3'+"321cba"="3321cba". Yes!
    # "level": reverse="level", first char 'l', output 'l'+"level"="llevel". Yes!
    # "Zebra": reverse="arbeZ", first char 'a', output 'a'+"arbeZ"="aarbeZ". Yes!
    # "bananaUPPER": reverse="RREPPUananab", first char 'R', output 'R'+"RREPPUananab"="RRREPPUananab"? 
    #   But observed "RREPPUananab". Hmm that's just reverse, no duplication!
    #   Wait observed: "RREPPUananab". reverse("bananaUPPER") = "RREPPUananab". So no extra char here.
    #   Contradiction. Unless... let's recount. "bananaUPPER" reversed: R E P P U a n a n a b = "REPPUananab"? 
    #   Let's carefully reverse "bananaUPPER": chars b,a,n,a,n,a,U,P,P,E,R -> reversed R,E,P,P,U,a,n,a,n,a,b = "REPPUananab".
    #   Observed "RREPPUananab" = 'R'+"REPPUananab". So there IS duplication! I misread.
    #   Yes: "RREPPUananab" = R + "REPPUananab". Good, consistent.
    # "Hello World function lazy": reverse = "yzal noitcnuf dlroW olleH". First char 'y'.
    #   Output should be 'y'+"yzal noitcnuf dlroW olleH" = "yyzal noitcnuf dlroW olleH".
    #   But observed "olleH dlroW noitcnuf yyzal". That's different!
    #   Hmm. Observed is reverse of word order? Let's see: reverse whole string then... no.
    #   Observed words: olleH dlroW noitcnuf yyzal. That's each word reversed, in original order, with last word getting extra char?
    #   Actually "olleH"=reverse("Hello"), "dlroW"=reverse("World"), "noitcnuf"=reverse("function"), "yyzal"='y'+reverse("lazy").
    #   So maybe: reverse each word, and duplicate first char of the whole reversed... no.
    #   Wait, maybe the rule is: reverse the entire string, then duplicate the first character, BUT the observed for multi-word is different.
    #   Let me re-examine. reverse("Hello World function lazy") = "yzal noitcnuf dlroW olleH".
    #   Duplicate first char: "yyzal noitcnuf dlroW olleH". Observed: "olleH dlroW noitcnuf yyzal".
    #   Observed is the reverse of "yyzal noitcnuf dlroW olleH"? Reverse of that = "HleH olleH..." no.
    #   Actually reverse of "yyzal noitcnuf dlroW olleH" = "HleH olleH..." let me just: reverse("yyzal noitcnuf dlroW olleH") = "HleH olleH..." no.
    #   Let's reverse "olleH dlroW noitcnuf yyzal": = "lazyy function World Hello"? No.
    #   Hmm, "olleH dlroW noitcnuf yyzal" reversed char by char = "lazyy function World Hello"? 
    #   reverse("olleH dlroW noitcnuf yyzal") = "lazyy function World Hello"? Let's do: last char 'l','a','z','y','y' -> "lazyy", space, "noitcnuf" reversed = "function", space, "dlroW" reversed="World", space, "olleH" reversed="Hello". So = "lazyy function World Hello". Not input.
    #   So it's not a simple reverse.
    #   Maybe: reverse each word, keep order, and duplicate first char of the reversed LAST word? 
    #   "lazy" reversed "yzal", duplicate first char 'y' -> "yyzal". Others just reversed. That matches!
    #   But why last word? Maybe it's: reverse each word, then duplicate first char of the whole output? No, output starts "olleH" not duplicated.
    #   Alternatively: reverse the string, then duplicate first char, but then reverse word order? 
    #   reverse whole = "yzal noitcnuf dlroW olleH", duplicate first 'y' -> "yyzal noitcnuf dlroW olleH", then reverse word order -> "olleH dlroW noitcnuf yyzal". YES! That matches!
    #   So rule: reverse whole string, duplicate first char, then reverse the order of words (split by space)?
    #   But wait for single words there's no space so word order reversal does nothing. Consistent!
    #   Check "abc123": reverse "321cba", dup first '3' -> "3321cba", no spaces, same. Yes.
    #   " Zebralower": reverse "rewolarbeZ " (trailing space), dup first 'r' -> "rrewolarbeZ ", reverse word order: split by space -> ["rrewolarbeZ", ""], reversed -> ["", "rrewolarbeZ"], join -> " rrewolarbeZ"? That gives leading space. Observed "rrewolarbeZ" no leading space.
    #   Hmm. Maybe strip? Or maybe the rule is different.
    #   Let's reconsider. Maybe: reverse each word individually, keep word order, but duplicate first char of the reversed string's first char applied to... 
    #   Actually simpler: reverse each word, keep order. Then duplicate the first character of the LAST word's reversed form? For "lazy"->"yzal"->"yyzal". For single word "abc123"->"321cba"->"3321cba". For "bananaUPPER"->"REPPUananab"->"RREPPUananab". For " Zebralower": words ["","Zebralower"], reversed each: ["","rewolarbeZ"], duplicate first char of last word 'r' -> "rrewolarbeZ", join with space -> " rrewolarbeZ". Still leading space.
    #   Observed "rrewolarbeZ" no leading space. Maybe leading/trailing spaces stripped? Or maybe split() without keeping empties.
    #   If we split by whitespace (default split()), " Zebralower".split() = ["Zebralower"], reversed "rewolarbeZ", dup 'r' -> "rrewolarbeZ". Matches!
    #   Check "Hello World function lazy".split() = ["Hello","World","function","lazy"], reversed each: ["olleH","dlroW","noitcnuf","yzal"], dup first char of last word 'y' -> "yyzal", join -> "olleH dlroW noitcnuf yyzal". Matches!
    #   Check "abc123".split()=["abc123"], reversed "321cba", dup '3' -> "3321cba". Matches.
    #   Check "level".split()=["level"], reversed "level", dup 'l' -> "llevel". Matches.
    #   Check "bananaUPPER".split()=["bananaUPPER"], reversed "REPPUananab", dup 'R' -> "RREPPUananab". Matches.
    #   Check "Zebra".split()=["Zebra"], reversed "arbeZ", dup 'a' -> "aarbeZ". Matches.
    # So rule: split input on whitespace, reverse each word, then duplicate the first character of the last reversed word (prepend it), join with single spaces.
    # Wait, but for multi-word, only last word gets duplication. Let me double check "Hello World function lazy": last word "lazy" reversed "yzal", dup 'y' -> "yyzal". Others plain reversed. Yes.
    # But is it "last word" or "the whole reversed string's first char"? For multi-word, whole reversed string's first char is 'y' (from "yzal..."), same as last word's reversed first char. So ambiguous. For single word same. 
    # For " Zebralower", whole reversed string (after split join?) Hmm.
    # Let's think: maybe the rule is: reverse the entire string (including spaces), duplicate the first character, then... no.
    # Alternative: reverse each word, join with spaces, then duplicate the first character of the result? For "Hello World function lazy": reversed words joined = "olleH dlroW noitcnuf yzal", first char 'o', dup -> "oolleH...". Not observed.
    # So duplication is on the last word's reversed form (or equivalently the first char of the reversed whole string before word reordering). 
    # Actually simplest consistent: reverse each word, then take the last word's reversed form and prepend its first char to it. Join.
    # But why last word? Maybe it's: reverse the whole string, duplicate first char, then reverse word order. For " Zebralower": reverse whole = "rewolarbeZ " (trailing space), dup first 'r' -> "rrewolarbeZ ", reverse word order: split by space -> ["rrewolarbeZ",""], reversed -> ["","rrewolarbeZ"], join with space -> " rrewolarbeZ". Leading space. Observed no leading space. Unless we strip.
    # If we strip the final result: " rrewolarbeZ".strip() = "rrewolarbeZ". Matches!
    # Check "Hello World function lazy": reverse whole "yzal noitcnuf dlroW olleH", dup 'y' -> "yyzal noitcnuf dlroW olleH", reverse word order -> "olleH dlroW noitcnuf yyzal". No leading/trailing space. Matches.
    # Check single words: no spaces, word order reversal does nothing. Matches.
    # So two equivalent formulations. The "reverse each word, dup first char of last word" is simpler and handles spaces by split().
    # But what about multiple spaces or tabs? Unknown. I'll use split() which collapses whitespace.
    # Also what about empty string? split() gives [], join gives "". Dup? No last word. Return "".
    # What about punctuation? Just treat as characters.
    # Let me go with: words = s.split(); if not words: return ""; rev = [w[::-1] for w in words]; rev[-1] = rev[-1][0] + rev[-1]; return " ".join(rev).
    # Wait check "abc123": rev=["321cba"], rev[-1]="3321cba". Good.
    # Check "level": rev=["level"], rev[-1]="llevel". Good.
    # Check " Zebralower": split -> ["Zebralower"], rev=["rewolarbeZ"], rev[-1]="rrewolarbeZ". Good.
    # Check "Hello World function lazy": rev=["olleH","dlroW","noitcnuf","yzal"], rev[-1]="yyzal". Join -> "olleH dlroW noitcnuf yyzal". Good.
    # Check "bananaUPPER": rev=["REPPUananab"], rev[-1]="RREPPUananab". Good.
    # Check "Zebra": rev=["arbeZ"], rev[-1]="aarbeZ". Good.
    # All match! 
    # Edge: what if last word is empty? split() won't produce empty. Good.
    # What about non-space whitespace like tab? split() handles.
    # What about the duplication when last reversed word is empty? Can't happen with split().
    # I'll implement this.
    try:
        s = probe["inputs"]
        out = []
        for x in s:
            if not isinstance(x, str):
                x = str(x)
            words = x.split()
            if not words:
                out.append("")
                continue
            rev = [w[::-1] for w in words]
            if rev[-1]:
                rev[-1] = rev[-1][0] + rev[-1]
            out.append(" ".join(rev))
        return {"outputs": out}
    except Exception:
        return {"outputs": ["" for _ in probe.get("inputs", [])]}
