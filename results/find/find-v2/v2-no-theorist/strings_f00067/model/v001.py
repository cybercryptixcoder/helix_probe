def predict(probe):
    # Observations from E1:
    # "abc123" -> "3321cba": reverse the string, then map each digit d to 9-d? 
    #   reverse("abc123") = "321cba"; observed "3321cba" -> first char '3' extra? 
    #   Actually observed "3321cba" = "3" + "321cba"? Let's check: reverse is "321cba", observed "3321cba" has extra leading '3'.
    #   Hmm. Maybe digit mapping: '1'->'3'? Let's re-examine.
    # "level" -> "llevel": prepend 'l'? reverse("level")="level", observed "llevel" = "l"+"level". So prepend first char? first char of input is 'l'. 
    # " Zebralower" -> "rrewolarbeZ": reverse(" Zebralower") = "rewolarbeZ " (with trailing space). Observed "rrewolarbeZ" = "r"+"rewolarbeZ"? reverse gives "rewolarbeZ " -> stripping space gives "rewolarbeZ", prepend 'r'? first char of reversed is 'r'. So prepend first char of reversed string, drop trailing space?
    # "Hello World function lazy" -> "olleH dlroW noitcnuf yyzal": reverse = "yzal noitcnuf dlroW olleH". Observed "olleH dlroW noitcnuf yyzal" - that's not a simple reverse. Words reversed in order? "lazy function World Hello" reversed chars each? "yzal noitcnuf dlroW olleH". Observed: "olleH dlroW noitcnuf yyzal" = words in original order but each word reversed? "Hello"->"olleH", "World"->"dlroW", "function"->"noitcnuf", "lazy"->"yzal". But observed has "yyzal" (double y). Hmm.
    # "bananaUPPER" -> "RREPPUananab": reverse = "REPPUananab". Observed "RREPPUananab" = "R"+"REPPUananab". Prepend first char of reversed.
    # "Zebra" -> "aarbeZ": reverse = "arbeZ". Observed "aarbeZ" = "a"+"arbeZ". Prepend first char of reversed.
    # So pattern: reverse the string, then prepend the first character of the reversed string (i.e., last char of original).
    # Check "level": reverse="level", first char 'l', prepend -> "llevel" ✓
    # " Zebralower": reverse="rewolarbeZ ", first char 'r', prepend -> "rrewolarbeZ " but observed "rrewolarbeZ" (no trailing space). Maybe strip? Or maybe space handling.
    # "Hello World function lazy": reverse="yzal noitcnuf dlroW olleH", first char 'y', prepend -> "yyzal noitcnuf dlroW olleH". Observed "olleH dlroW noitcnuf yyzal" - that's different! It's word order reversed? Let's see: observed words: "olleH", "dlroW", "noitcnuf", "yyzal". Original words: "Hello","World","function","lazy". Each word reversed: "olleH","dlroW","noitcnuf","yzal". Then prepend first char of reversed whole? Hmm "yyzal" has double y.
    # Wait: maybe the operation is: reverse each word, keep word order, then prepend first char of the reversed full string? No.
    # Let's reconsider: maybe it's reverse the whole string, then for each word... no.
    # Actually observed "olleH dlroW noitcnuf yyzal": if we reverse each word in place: "olleH dlroW noitcnuf yzal". Then prepend first char of that? first char 'o'? No.
    # Double y in "yyzal": original "lazy" reversed is "yzal". Prepending 'y' gives "yyzal". So the prepend happens per-word? For "Hello" reversed "olleH", prepend 'o'? would be "oolleH" but observed "olleH". Hmm.
    # Let's check "abc123": reverse="321cba", prepend first char '3' -> "3321cba" ✓ (matches!)
    # "bananaUPPER": reverse="REPPUananab", prepend 'R' -> "RREPPUananab" ✓
    # "Zebra": reverse="arbeZ", prepend 'a' -> "aarbeZ" ✓
    # "level": reverse="level", prepend 'l' -> "llevel" ✓
    # " Zebralower": reverse="rewolarbeZ ", prepend 'r' -> "rrewolarbeZ " but observed "rrewolarbeZ". Maybe trailing space stripped? Or maybe the space is treated specially.
    # "Hello World function lazy": reverse="yzal noitcnuf dlroW olleH", prepend 'y' -> "yyzal noitcnuf dlroW olleH". Observed "olleH dlroW noitcnuf yyzal". That's the reverse of "yyzal noitcnuf dlroW olleH"? Reverse of that is "HleH olleH..." no.
    # Wait: observed "olleH dlroW noitcnuf yyzal" - if we reverse the whole observed: "lazyy function World Hello" no.
    # Let's reverse observed: "lazyy function World Hello" -> hmm "lazyy" not "lazy".
    # Actually maybe the operation is: split into words, reverse each word, then reverse word order? Let's test: "Hello World function lazy" -> reverse each word: "olleH dlroW noitcnuf yzal" -> reverse word order: "yzal noitcnuf dlroW olleH". Not observed.
    # Observed: "olleH dlroW noitcnuf yyzal". Words: "olleH","dlroW","noitcnuf","yyzal". These are reversed words in original order, except last word "yyzal" has extra y.
    # Maybe the rule is: reverse the whole string, then prepend first char of reversed string, but for multi-word... no.
    # Let's check: reverse whole = "yzal noitcnuf dlroW olleH". Prepend first char 'y' -> "yyzal noitcnuf dlroW olleH". Observed is "olleH dlroW noitcnuf yyzal" which is the reverse of "yzal noitcnuf dlroW olleH" with extra y? Reverse of "yzal noitcnuf dlroW olleH" is "HleH olleH..." no, reverse is "Hello World function lazy" reversed char by char = "yzal noitcnuf dlroW olleH". 
    # Observed "olleH dlroW noitcnuf yyzal" reversed char by char = "lazyy function World Hello". Hmm.
    # Wait: "olleH dlroW noitcnuf yyzal" - if we reverse each word: "Hello World function lazy" with "yyzal"->"lazyy". So it's like reverse each word, but last word got extra char.
    # Maybe the rule: reverse the string, then prepend first char of reversed string, BUT the "reverse" is done per word? No, "abc123" is one word.
    # Let's test hypothesis: reverse each word, then prepend first char of the reversed whole string to the first word? For "Hello World function lazy": reverse each word = "olleH dlroW noitcnuf yzal". Prepend first char of reversed whole ('y') to... which word? If to last word: "yzal" -> "yyzal". That matches! And for single word, it's the same word.
    # Check "abc123": one word, reverse = "321cba", prepend first char of reversed whole ('3') to the word -> "3321cba" ✓
    # "level": one word, reverse="level", prepend 'l' -> "llevel" ✓
    # " Zebralower": one word (with leading space), reverse="rewolarbeZ ", first char 'r', prepend to word -> "rrewolarbeZ " but observed "rrewolarbeZ". Maybe trailing space stripped? Or maybe leading space is part of word and reversed to trailing, then stripped.
    # "bananaUPPER": one word, reverse="REPPUananab", prepend 'R' -> "RREPPUananab" ✓
    # "Zebra": one word, reverse="arbeZ", prepend 'a' -> "aarbeZ" ✓
    # So rule: split on spaces? For "Hello World function lazy", split into words, reverse each word, then prepend first char of the reversed whole string (which is last char of original) to the LAST word? Or to the first word? Observed prepend to last word "yzal"->"yyzal". But for single word, it's the only word.
    # Wait, maybe it's simpler: reverse the whole string, then prepend first char of reversed string, but the "reverse" is actually reverse each word and keep order? No.
    # Let's test: reverse whole string "yzal noitcnuf dlroW olleH". If we then reverse the order of words? "olleH dlroW noitcnuf yzal". Then prepend first char of reversed whole ('y') to last word -> "yyzal". That gives "olleH dlroW noitcnuf yyzal" ✓!
    # So: reverse whole string, then reverse word order, then prepend first char of reversed whole to last word? That's convoluted.
    # Alternative: reverse each word, keep order, then prepend first char of reversed whole to last word. Same result.
    # Let's check " Zebralower": split on space? " Zebralower" -> ["", "Zebralower"]? If split on space, first word empty. Reverse each: ["", "rewolarbeZ"]. Prepend first char of reversed whole ('r') to last word -> "rrewolarbeZ". Join with space -> " rrewolarbeZ"? But observed "rrewolarbeZ" no leading space. Hmm.
    # Maybe the rule is: reverse the string, then prepend the first character of the reversed string to the result, but if there's a space, something else.
    # Let's look at " Zebralower" -> "rrewolarbeZ". Reverse = "rewolarbeZ ". If we strip trailing space: "rewolarbeZ". Prepend 'r' -> "rrewolarbeZ" ✓. So maybe strip whitespace after reversing?
    # For "Hello World function lazy": reverse = "yzal noitcnuf dlroW olleH". Strip? No leading/trailing spaces. Prepend 'y' -> "yyzal noitcnuf dlroW olleH". But observed is "olleH dlroW noitcnuf yyzal". That's the reverse of the words? 
    # Wait: "yyzal noitcnuf dlroW olleH" reversed word order = "olleH dlroW noitcnuf yyzal" ✓! So maybe the operation is: reverse the string, prepend first char, then reverse word order? But for single word, no change.
    # Check "abc123": reverse="321cba", prepend '3' -> "3321cba", reverse word order (one word) -> same ✓.
    # "level": reverse="level", prepend 'l' -> "llevel", one word ✓.
    # " Zebralower": reverse="rewolarbeZ ", prepend 'r' -> "rrewolarbeZ ", reverse word order? Split on space: ["rrewolarbeZ", ""] -> reverse -> ["", "rrewolarbeZ"] -> join with space -> " rrewolarbeZ". Observed "rrewolarbeZ". Hmm, leading space issue.
    # Maybe the rule is: reverse the string, then prepend first char of reversed string, then reverse the order of characters? No.
    # Let's reconsider: maybe it's simply: reverse the string, then prepend the last character of the original string. And for multi-word, the "reverse" is done per word? Let's test: "Hello World function lazy" -> reverse each word: "olleH dlroW noitcnuf yzal". Prepend last char of original ('y') to the whole? "yolleH dlroW noitcnuf yzal" no.
    # Observed "olleH dlroW noitcnuf yyzal": last word "yyzal" = 'y' + "yzal". "yzal" is reverse of "lazy". So prepend last char of original to the reversed last word? But for single word, it's the same.
    # Check "abc123": last char '3', reverse="321cba", prepend '3' -> "3321cba" ✓.
    # "level": last char 'l', reverse="level", prepend 'l' -> "llevel" ✓.
    # "bananaUPPER": last char 'R', reverse="REPPUananab", prepend 'R' -> "RREPPUananab" ✓.
    # "Zebra": last char 'a', reverse="arbeZ", prepend 'a' -> "aarbeZ" ✓.
    # " Zebralower": last char 'r', reverse="rewolarbeZ ", prepend 'r' -> "rrewolarbeZ " but observed "rrewolarbeZ". Maybe strip trailing space? Or maybe the space is not part of the word? If we strip the input first? " Zebralower".strip() = "Zebralower", reverse="rewolarbeZ", prepend 'r' -> "rrewolarbeZ" ✓. But then "Hello World function lazy" has spaces inside, not stripped.
    # So maybe: strip leading/trailing whitespace, then reverse the string, then prepend the last character of the stripped string? For " Zebralower": stripped="Zebralower", last char 'r', reverse="rewolarbeZ", prepend 'r' -> "rrewolarbeZ" ✓.
    # For "Hello World function lazy": stripped same, last char 'y', reverse="yzal noitcnuf dlroW olleH", prepend 'y' -> "yyzal noitcnuf dlroW olleH". But observed is "olleH dlroW noitcnuf yyzal". That's different! So my earlier idea of reversing word order after prepending? Let's test: "yyzal noitcnuf dlroW olleH" reverse word order -> "olleH dlroW noitcnuf yyzal" ✓.
    # So the rule might be: strip, reverse the string, prepend last char of stripped string, then reverse the order of words? But for single word, no change.
    # Check "abc123": strip same, reverse="321cba", prepend '3' -> "3321cba", one word -> same ✓.
    # "level": reverse="level", prepend 'l' -> "llevel", one word ✓.
    # "bananaUPPER": reverse="REPPUananab", prepend 'R' -> "RREPPUananab", one word ✓.
    # "Zebra": reverse="arbeZ", prepend 'a' -> "aarbeZ", one word ✓.
    # " Zebralower": strip="Zebralower", reverse="rewolarbeZ", prepend 'r' -> "rrewolarbeZ", one word ✓.
    # So the rule: s = input.strip(); r = s[::-1]; p = s[-1] + r; then reverse the order of words in p (split on space, reverse list, join). But wait, for "Hello World function lazy": s="Hello World function lazy", r="yzal noitcnuf dlroW olleH", p="yyzal noitcnuf dlroW olleH", reverse words -> "olleH dlroW noitcnuf yyzal" ✓.
    # But is the word reversal always applied? For single word, no effect. For " Zebralower", after strip it's one word, no effect.
    # What about multiple spaces? We don't have evidence. Let's assume split on single space and join with single space.
    # Also, what about empty string? s="" -> s[-1] error. Handle: if empty, return "".
    # What about strings with only spaces? strip -> "" -> return "".
    # Let's implement this hypothesis.
    # But wait: is the word reversal really part of the rule? Let's check if there's a simpler explanation: maybe the operation is: reverse each word, then prepend last char of original to the last word? For "Hello World function lazy": reverse each word: "olleH dlroW noitcnuf yzal", prepend 'y' to last word -> "yyzal" -> "olleH dlroW noitcnuf yyzal" ✓. For single word, same as reverse and prepend. For " Zebralower": strip? If we don't strip, reverse each word: " Zebralower" split on space -> ["", "Zebralower"] -> reverse each: ["", "rewolarbeZ"] -> prepend last char 'r' to last word -> "rrewolarbeZ" -> join with space -> " rrewolarbeZ" (leading space). Observed no leading space. So strip is needed.
    # So: strip, split on space, reverse each word, prepend last char of stripped string to the last word, join with space. But for "Hello World function lazy", last char 'y', last word reversed "yzal" -> "yyzal" ✓.
    # Check "abc123": one word, reverse "321cba", prepend '3' -> "3321cba" ✓.
    # This is equivalent to: strip, reverse whole string, prepend last char, then reverse word order? Let's verify: reverse whole "yzal noitcnuf dlroW olleH", prepend 'y' -> "yyzal noitcnuf dlroW olleH", reverse word order -> "olleH dlroW noitcnuf yyzal" ✓. Same.
    # Which is more natural? The per-word reverse then prepend to last word is simpler to implement.
    # Let's go with: s = input.strip(); if not s: return ""; words = s.split(" "); rev_words = [w[::-1] for w in words]; last = s[-1] + rev_words[-1]; rev_words[-1] = last; return " ".join(rev_words).
    # Test "Hello World function lazy": s="Hello World function lazy", words=["Hello","World","function","lazy"], rev=["olleH","dlroW","noitcnuf","yzal"], last='y'+"yzal"="yyzal", join -> "olleH dlroW noitcnuf yyzal" ✓.
    # Test " Zebralower": s="Zebralower", words=["Zebralower"], rev=["rewolarbeZ"], last='r'+"rewolarbeZ"="rrewolarbeZ", join -> "rrewolarbeZ" ✓.
    # Test "abc123": s="abc123", words=["abc123"], rev=["321cba"], last='3'+"321cba"="3321cba" ✓.
    # Test "level": s="level", rev="level", last='l'+"level"="llevel" ✓.
    # Test "bananaUPPER": s="bananaUPPER", rev="REPPUananab", last='R'+"REPPUananab"="RREPPUananab" ✓.
    # Test "Zebra": s="Zebra", rev="arbeZ", last='a'+"arbeZ"="aarbeZ" ✓.
    # All match!
    # What about multiple spaces? We'll assume split on single space and join with single space. If there are multiple spaces, split(" ") will produce empty strings. We'll handle by splitting on whitespace? But evidence only has single spaces. Let's use split() which splits on any whitespace and removes empty strings, then join with single space. But that would change multiple spaces to single. We don't have evidence. Safer to use split(" ") and keep empty strings? For " Zebralower", split(" ") gives ["", "Zebralower"], but we strip first so no leading space. For internal multiple spaces, we don't know. Let's use split() to be safe? But then "a  b" -> ["a","b"] -> join "a b". We don't know. I'll use split() and join with single space, as it's simpler and handles whitespace.
    # Actually, the evidence "Hello World function lazy" has single spaces. I'll use split() and join with " ".
    # Also, what about tabs/newlines? Not tested. Use split() which handles all whitespace.
    # So final: s = input.strip(); if not s: return ""; words = s.split(); rev = [w[::-1] for w in words]; rev[-1] = s[-1] + rev[-1]; return " ".join(rev).
    # But wait: s[-1] is last char of stripped string. For "Hello World function lazy", s[-1]='y'. Good.
    # What if the string has trailing spaces? strip removes them, so s[-1] is last non-space char. Good.
    # What if the string is all spaces? strip -> "" -> return "".
    # What if the string is empty? return "".
    # Let's implement.
    def predict(probe):
        outs = []
        for x in probe.get("inputs", []):
            if not isinstance(x, str):
                outs.append("")
                continue
            s = x.strip()
            if not s:
                outs.append("")
                continue
            words = s.split()
            rev = [w[::-1] for w in words]
            rev[-1] = s[-1] + rev[-1]
            outs.append(" ".join(rev))
        return {"outputs": outs}
    return predict(probe)
