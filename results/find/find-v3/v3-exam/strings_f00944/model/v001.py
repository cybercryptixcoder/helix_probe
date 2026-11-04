def predict(probe):
    # Last char is replaced by the char before it in the alphabet? Let's check.
    # "abc123" -> "abc123" (last char '3' -> '3'? no change)
    # "level" -> "levem" ('l'->'m', next char!)
    # " Zebralower" -> " Zebralowes" ('r'->'s', next char)
    # "Hello World function lazy" -> "...lazz" ('y'->'z', next char)
    # "bananaUPPER" -> "bananaUPPF" ('R'->'F'? no... 'R'->'S'? no, 'F'?)
    #   Wait: 'R' -> 'F'? That's not next. Hmm. Actually 'R'->'S' would be next.
    #   Let me recheck: "bananaUPPER" -> "bananaUPPF". Last char 'R' -> 'F'.
    #   Hmm 'R' + 1 = 'S'. Not F. 
    #   Wait maybe it's not last char. "bananaUPPER" length 11. Output "bananaUPPF" length 10.
    #   So last char dropped? "bananaUPPE" + "F"? No, "bananaUPPF" = b a n a n a U P P F.
    #   Original: b a n a n a U P P E R. Output: b a n a n a U P P F.
    #   So 'E' -> 'F' (next char), and 'R' dropped? Or last char 'R' replaced by next of 'E'?
    # "Zebra" -> "Zebrb": Z e b r a -> Z e b r b. 'a'->'b' next char. Length same (5).
    # So for "bananaUPPER": length 11 -> 10. Hmm.
    #   Actually maybe last char replaced by next of second-to-last? 'E'->'F', drop 'R'?
    # Let's check "abc123" -> "abc123". Last char '3'. Next of '3'? '4'. But output is '3'.
    #   So digits unchanged? Or '3'->'3'? 
    # "level" -> "levem": last 'l'->'m'. Next char.
    # " Zebralower" -> " Zebralowes": last 'r'->'s'. Next char.
    # "lazy" -> "lazz": 'y'->'z'. Next char.
    # "Zebra" -> "Zebrb": 'a'->'b'. Next char.
    # "bananaUPPER": 'R'->? If next char of 'R' is 'S', not 'F'. 
    #   But if we take 'E' (second to last) -> 'F', and drop 'R'? That gives "bananaUPPF". Yes!
    #   Why drop? Maybe because 'R' is uppercase and... hmm.
    #   Or maybe: last char replaced by next char, but if last char is 'Z' or 'z' or '9'? 
    #   'R' -> 'S' not F. So that's not it.
    #   Wait maybe it's: replace last char with next char, but 'R'->'S'... no.
    #   Let me reconsider: maybe the rule is last char -> next char, but for "bananaUPPER" 
    #   something else. Actually maybe 'R' -> 'S'? Output shows 'F'. 
    #   Hmm, unless I misread. "bananaUPPF" - b,a,n,a,n,a,U,P,P,F. Yes F.
    #   'E'->'F' is next. 'R' dropped. 
    #   Could be: if last char is uppercase, replace second-to-last with next and drop last?
    #   But "Zebra" last 'a' lowercase -> 'b'. "level" 'l'->'m'. 
    #   "abc123" last '3' -> '3'? digits unchanged.
    #   Let's hypothesize: last char replaced by next char in alphabet if letter, 
    #   but for uppercase last char... hmm 'R'->? 
    #   Actually wait: maybe it's Caesar shift on last char by +1, wrapping? 'R'+1='S'. Not F.
    #   Let me reconsider "bananaUPPER". Maybe the output is "bananaUPPF" meaning last char 'R' -> 'F'?
    #   'R' is 18th letter, 'F' is 6th. Difference -12. Not obvious.
    #   Hmm, but 'E'->'F' is +1. So maybe the last TWO chars "ER" -> "F"? 
    #   Like "ER" -> next of E = F, drop R? That's weird.
    #   Alternative: maybe it's the last char, and 'R' -> 'F' because... no.
    #   Let me just go with: replace last char with next letter (a->b, ..., z->a? or z->?), 
    #   digits unchanged, and handle "bananaUPPER" specially? No, can't special-case.
    #   Actually maybe the rule: last char -> next char, and if result would be... 
    #   Hmm. Let me look again: "bananaUPPER" has 11 chars, output 10. 
    #   Maybe the rule is: shift last char +1, but if last char is uppercase letter, 
    #   shift the char before it and remove last? That's ad hoc.
    #   Wait — maybe it's simpler: the last character is replaced by the NEXT character, 
    #   but "R" -> "S"? No output is F.
    #   Let me recount "bananaUPPER": b-a-n-a-n-a-U-P-P-E-R = 11 chars.
    #   "bananaUPPF": b-a-n-a-n-a-U-P-P-F = 10 chars.
    #   So 'E'->'F' and 'R' removed. 
    #   Hmm what if rule: replace last char with next char, but if last char is 'R'... no.
    #   What if the rule operates on last char: 'R' -> 'F'? R=82, F=70. -12.
    #   'a'->'b' +1, 'l'->'m' +1, 'r'->'s' +1, 'y'->'z' +1, '3'->'3' +0.
    #   So letters +1, digits +0. But 'R'->'F' is -12. Contradiction.
    #   Unless... "bananaUPPER" output is actually "bananaUPPF" where the last char 
    #   'R' was replaced by 'F'? Or is it that 'E'->'F' and 'R' dropped because 
    #   'R' is the last and... 
    #   OH. Maybe the rule is: replace last char with next char, but if the last char 
    #   is 'R', next is 'S'... no.
    #   Let me try: maybe it's not last char but last LETTER, and 'R' is a letter. 
    #   Hmm.
    #   Actually, maybe the transformation is: shift the last character forward by 1, 
    #   but for uppercase 'R'... 
    #   Wait, what if it's a Caesar shift on the last char by +1, but 'R' -> 'S'? 
    #   The output clearly shows F though.
    #   Let me reconsider: maybe the rule is: the last char is replaced by the char 
    #   that comes after it in the string's alphabet... no.
    #   New idea: maybe it's the last char, and 'R' -> 'F' because it's ROT? 
    #   R (18) -> F (6): -12. E (5) -> F (6): +1. 
    #   Hmm, what if the rule is: replace last char with next char, but if last char 
    #   is uppercase, replace the SECOND-to-last char with next and drop last? 
    #   For "Zebra", last 'a' lowercase -> 'b'. OK.
    #   For "bananaUPPER", last 'R' uppercase -> replace 'E' with 'F', drop 'R'. 
    #   That fits! But is it a real rule? Seems arbitrary.
    #   Alternative: maybe the rule is: last char -> next char, but if that char is 
    #   uppercase, it wraps differently? 'R'->'S' not F.
    #   Hmm, let me just test: what if the rule is simply "replace last char with next 
    #   char in alphabet, digits unchanged, and for 'R' specifically..." no.
    #   I'll go with: last char replaced by next char; if last char is uppercase letter, 
    #   replace second-to-last with next and drop last. Mark with "?".
    #   Actually wait, simpler: maybe the rule is "increment last character", where 
    #   increment means next in sequence a,b,...,z,A,B,...,Z,0,1,...,9? 
    #   'R' -> 'S' still. Not F.
    #   Hmm. Let me reconsider the data. "bananaUPPER" -> "bananaUPPF".
    #   What if it's not the last char but the last char 'R' becomes 'F' via some 
    #   other rule like ROT13? R->E, not F. ROT? 
    #   R=17 (0-indexed), F=5. 17-12=5. E=4, F=5. +1.
    #   What if the rule is: last char -> next char, but if it's 'R'... 
    #   I think the most likely intended rule: replace last char with next char, 
    #   and "bananaUPPER" is a case where... hmm.
    #   Actually! Maybe the rule is: the last char is replaced by the next char, 
    #   but if the last char is uppercase, it's replaced by the next char of the 
    #   PREVIOUS char and the last is dropped? That's what I said.
    #   Or maybe: for uppercase last char, the whole thing... 
    #   Let me just go with a rule that fits all: 
    #   - If last char is lowercase letter: replace with next lowercase (z->a?).
    #   - If last char is digit: unchanged.
    #   - If last char is uppercase letter: replace second-to-last char with next 
    #     (if it's a letter) and drop last char.
    #   This fits all 6 examples. Mark with "?".
    #   Actually "abc123" last is '3' digit -> unchanged. Good.
    #   But what about "Zebra" last 'a' -> 'b'. Good.
    #   Hmm but "bananaUPPER": second-to-last 'E' -> 'F', drop 'R'. Good.
    #   But what if second-to-last isn't a letter? Edge case.
    #   I'll implement this best guess.
    def transform(s):
        if not s:
            return s
        last = s[-1]
        if last.isdigit():
            return s
        if last.islower():
            if last == 'z':
                return s[:-1] + 'a'
            return s[:-1] + chr(ord(last) + 1)
        if last.isupper():
            if len(s) < 2:
                return s
            prev = s[-2]
            if prev.isalpha():
                if prev == 'z':
                    newprev = 'a'
                elif prev == 'Z':
                    newprev = 'A'
                else:
                    newprev = chr(ord(prev) + 1)
                return s[:-2] + newprev
            else:
                return s[:-1]
        return s
    return {"outputs": [transform(x) for x in probe["inputs"]]}
