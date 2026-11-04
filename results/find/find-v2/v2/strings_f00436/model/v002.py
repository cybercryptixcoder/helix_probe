def predict(probe):
    # Reverse the string, then insert "I" [E1, E2]
    # Insert position is at the middle of the reversed string, but biased toward the front:
    #   len 1 -> pos 1 ("a"->"aI"), len 2 -> 1 ("ab"->"bIa"), len 3 -> 2 ("abc"->"cbIa")
    #   len 4 -> 2 ("abcd"->"dcIba"), len 5 -> 3 ("abcde"->"edcIba"), len 6 -> 3 ("abc123"->"321Icba")
    #   len 5 "ab cd" -> "Iba dc" (pos 0!), len 5 "xy z" -> "Iyx z" (pos 0!)
    #   len 2 "  " -> "I" (pos 0), len 11 -> 6, len 5 "Zebra" -> 3, len 11 "bananaUPPER" -> 6
    # Pattern: pos = (len+1)//2 normally, BUT if the reversed string contains a space, pos = 0? 
    #   "ab cd" reversed = "dc ba" contains space -> "Iba dc"?? No, output is "Iba dc" = "I"+"ba dc"
    #   Wait: "ab cd" reversed is "dc ba", but output is "Iba dc". That's not a reversal!
    #   "ab cd" -> "Iba dc": looks like "ba dc" + I at front. "ba dc" is NOT reverse of "ab cd" ("dc ba").
    #   Hmm, "ab cd" -> "Iba dc". Reverse of "ab cd" = "dc ba". Output "ba dc" reversed = "cd ab". 
    #   Actually "Iba dc" without I = "ba dc". Reverse of "ab cd" is "dc ba". Not equal.
    #   But "xy z" -> "Iyx z": without I = "yx z". Reverse of "xy z" = "z yx". Not equal.
    #   So for strings with spaces, something else happens. "ba dc" vs "dc ba"...
    #   "ab cd" split by space: ["ab","cd"]. Reversed words order? "cd ab". No.
    #   Maybe: reverse each word? "ba dc". YES! "ab"->"ba", "cd"->"dc", joined "ba dc". Then I at front.
    #   "xy z": words ["xy","z"] -> "yx z". YES! Then I at front -> "Iyx z". 
    #   "  ": words ["","",""] -> "" -> "I". YES!
    #   "Hello World function lazy" -> words reversed each: "olleH dlroW noitcnuf yzal", then I inserted.
    #     Output: "olleH dlroW noitcnufI yzal". So I inserted at pos 6 in "olleH dlroW noitcnuf yzal"? 
    #     len 26, (26+1)//2=13. But I is at index 20. Hmm.
    #   Wait, maybe it's not per-word reverse. Let me reconsider.
    #   "Hello World function lazy" reversed whole = "yzal noitcnuf dlroW olleH". Output "olleH dlroW noitcnufI yzal".
    #   That's NOT the reverse. Output words: "olleH","dlroW","noitcnufI","yzal". 
    #   Original words: "Hello","World","function","lazy". Each reversed: "olleH","dlroW","noitcnuf","yzal". 
    #   Joined: "olleH dlroW noitcnuf yzal". Insert I: "olleH dlroW noitcnufI yzal" -> I after "noitcnuf" (pos 20).
    #   len 26. pos 20? Not middle. Hmm.
    #   "ab cd" -> "ba dc", I at front (pos 0). len 5.
    #   "xy z" -> "yx z", I at front (pos 0). len 4.
    #   "  " -> "", I at pos 0. len 0.
    #   "Hello World function lazy" -> I at pos 20 in len 26 string.
    #   " Zebralower" -> "rewolarbeZ", I at pos 6. len 11. (11+1)//2=6. OK middle.
    #   "bananaUPPER" -> "REPPUananab", I at pos 6. len 11. middle.
    #   "Zebra" -> "arbeZ", I at pos 3. len 5. middle.
    #   "abc123" -> "321cba", I at pos 3. len 6. middle.
    #   "level" -> "level", I at pos 3. len 5. middle.
    #   So no-space strings: reverse whole, insert I at (len+1)//2.
    #   Space strings: reverse each word, join with space, then insert I... where?
    #     "ab cd" -> "ba dc", I at 0.
    #     "xy z" -> "yx z", I at 0.
    #     "  " -> "", I at 0.
    #     "Hello World function lazy" -> "olleH dlroW noitcnuf yzal", I at 20.
    #   Hmm inconsistent. Unless the rule is: reverse whole string, then insert I at (len+1)//2, 
    #     but ALSO reverse each word? Let's check "ab cd": reverse whole "dc ba", reverse each word "cd ab"? no.
    #   Alternative: the box reverses the string, then inserts I at middle. For "ab cd": reverse="dc ba", 
    #     middle pos (5+1)//2=3 -> "dc Iba"? But observed "Iba dc". Not matching.
    #   Let me try: maybe it reverses words individually AND reverses order? "ab cd"->"cd ab"->? no.
    #   Observed "Iba dc". If we take "ab cd", reverse each word -> "ba dc", then prepend I. 
    #     For "Hello...": reverse each word -> "olleH dlroW noitcnuf yzal", prepend I would give "IolleH...". 
    #     But observed I is at pos 20. So not prepend.
    #   Maybe: reverse each word, then insert I at (len+1)//2 of the RESULT?
    #     "ba dc" len 5, (5+1)//2=3 -> "ba I dc"? No, observed "Iba dc".
    #   Hmm. "Iba dc": I at 0. "olleH dlroW noitcnufI yzal": I at 20.
    #   What if insertion is at position = number of characters before the middle WORD boundary? 
    #   Or: insert I at the position of the middle character of the ORIGINAL string's reverse?
    #   Let me try: reverse whole string, then insert I at (len+1)//2, but ALSO the whole thing is 
    #     word-reversed? No.
    #   Let me look again: "ab cd" -> "Iba dc". Reverse of "ab cd" is "dc ba". "Iba dc" reversed is "cd abI". 
    #     Not helpful.
    #   "xy z" -> "Iyx z". Reverse of "xy z" is "z yx". "Iyx z" reversed "z xyI".
    #   Maybe the rule: split into words, reverse each word, then insert I at position = (len+1)//2 
    #     but counting only... no.
    #   Actually wait: "ba dc" - if we insert I at pos 0 for "ab cd" (len 5), and at pos 20 for len 26...
    #     Maybe pos depends on number of spaces? "ab cd" 1 space -> pos 0. "xy z" 1 space -> pos 0.
    #     "  " 2 spaces -> pos 0. "Hello World function lazy" 3 spaces -> pos 20.
    #   Hmm, 3 spaces -> 20? That's weird.
    #   Let me reconsider "Hello World function lazy". Maybe it's NOT word-reversed. 
    #     Reverse whole: "yzal noitcnuf dlroW olleH". Insert I at (26+1)//2=13: "yzal noitcnufIdlroW olleH". 
    #     Observed: "olleH dlroW noitcnufI yzal". That's the reverse of "yzal noitcnufIdlroW olleH"? 
    #     Reverse of observed: "lazy Ifunction dlroW olleH". Hmm no.
    #   Observed "olleH dlroW noitcnufI yzal". Reverse it: "lazy Ifunction dlroW olleH". 
    #     Original "Hello World function lazy". Reverse of original: "yzal noitcnuf dlroW olleH".
    #     So observed reversed = "lazy Ifunction dlroW olleH" vs original-reversed "yzal noitcnuf dlroW olleH".
    #     These differ: "lazy I" vs "yzal " and "function" vs "noitcnuf". So observed is word-reversed.
    #   OK so word-reverse confirmed for multi-word. Insertion position for word-reversed:
    #     "ba dc" (from "ab cd"): I at 0.
    #     "yx z" (from "xy z"): I at 0.
    #     "" (from "  "): I at 0.
    #     "olleH dlroW noitcnuf yzal": I at 20.
    #   What's special? Maybe insert I at the middle of the LAST word? 
    #     "ba dc": last word "dc", middle pos 1 -> "ba dIc"? No.
    #   Maybe insert I before the last word? "ba dc" -> "ba Idc"? No, observed "Iba dc".
    #   Maybe insert I at position = len of first word? "ba dc": first word "ba" len 2 -> pos 2 -> "baI dc"? No.
    #   Hmm. Let me count "olleH dlroW noitcnuf yzal": positions: o0 l1 l2 e3 H4 space5 d6 l7 r8 o9 W10 space11 n12 o13 i14 t15 c16 n17 u18 f19 space20 y21 z22 a23 l24. 
    #     I is at 20, which is right before " yzal" (the space before last word). So I inserted before the last word!
    #   "ba dc": before last word "dc" is after "ba " -> "ba Idc"? But observed "Iba dc". Hmm, I at 0, before first word.
    #   Wait, maybe I misread. "ab cd" -> "Iba dc". If I is before last word: "ba Idc". Not matching.
    #   Let me recount "Iba dc": I0 b1 a2 space3 d4 c5. So I at 0.
    #   "Iyx z": I0 y1 x2 space3 z4. I at 0.
    #   "I": just I.
    #   Hmm. So for short multi-word, I at 0; for long, I at 20 (before last word).
    #   Maybe the rule is: insert I at (len+1)//2 of the word-reversed string, but if that position 
    #     falls... no. "ba dc" len 5, (5+1)//2=3 -> "ba Idc". Not 0.
    #   Let me reconsider: maybe it's not word-reverse. Maybe it's reverse whole, then insert I at middle, 
    #     then... no.
    #   Actually, let me reconsider "ab cd" -> "Iba dc". What if the box reverses the whole string 
    #     "dc ba", then inserts I at position = (len+1)//2 = 3 -> "dc Iba". But observed "Iba dc". 
    #     "Iba dc" = reverse of "cd abI"? no.
    #   What if box does: reverse whole string, then move I to front if...? 
    #   Let me try a different hypothesis: the box reverses the string, then inserts I at the middle, 
    #     BUT the "middle" is computed on the original string and applied differently.
    #   Actually, maybe the box reverses each word AND reverses word order? "ab cd" -> "dc ba" (reverse order) 
    #     -> reverse each: "cd ab". No.
    #   Let me try: "ab cd" -> "Iba dc". If we reverse "ab cd" -> "dc ba". Then insert I at pos 0: "Idc ba". 
    #     Not matching.
    #   Hmm, "Iba dc". "ba dc" is reverse of each word. So word-reverse, then I at 0.
    #   "olleH dlroW noitcnufI yzal": word-reverse gives "olleH dlroW noitcnuf yzal", I at 20.
    #   What if I is inserted at position = (len+1)//2 of the ORIGINAL string, but in the word-reversed string?
    #     "ab cd" len 5, (5+1)//2=3 -> insert at 3 in "ba dc" -> "ba I dc"? No, "baIdc"? Observed "Iba dc".
    #   What if position = len - (len+1)//2? "ab cd": 5-3=2 -> "baI dc"? No.
    #   I'm stuck on the space case. Let me just note the pattern: 
    #     no space: reverse whole, insert I at (len+1)//2.
    #     space: reverse each word, insert I at... 0 for short, 20 for long. 
    #   Maybe the insertion position for space case is (len+1)//2 of the word-reversed string, 
    #     but I is placed at the START of the word containing that position? 
    #     "ba dc": pos 3 is 'd' (start of word "dc") -> insert before "dc" -> "ba Idc". No.
    #   Or I placed at the END of the word containing that position? pos 3 'd', end of word "dc" is pos 5 -> "ba dcI". No.
    #   Hmm. Let me try: maybe for space case, it's reverse whole string, insert I at (len+1)//2, 
    #     then reverse each word? "ab cd" reverse whole "dc ba", insert I at 3 "dc Iba", reverse each word 
    #     "cd abI"? no.
    #   I'll go with: if space present, reverse each word, insert I at position (len+1)//2 but 
    #     adjusted... Actually let me just check: maybe the rule is simpler than I think.
    #   "ab cd" -> "Iba dc". What if it's: reverse whole string -> "dc ba", then insert I at position 
    #     = number of chars before first space in original? "ab cd" first space at 2 -> pos 2 -> "dcI ba"? no.
    #   Let me try: maybe the box reverses the string, then inserts I at the middle, but for strings 
    #     with spaces it reverses words first. Let's just test: word-reverse "ab cd" = "ba dc". 
    #     Insert I at (len+1)//2 = 3: "ba Idc". Observed "Iba dc". Difference: I at 0 vs 3.
    #   What if insertion position = (len+1)//2 - number_of_spaces? "ab cd": 3-1=2 -> "baI dc"? no.
    #   What if = (len+1)//2 - 3*spaces? 3-3=0 -> "Iba dc". YES for "ab cd"!
    #     "xy z": len 4, (4+1)//2=2, spaces 1, 2-3=-1 -> clamp 0 -> "Iyx z". YES!
    #     "  ": len 2, (2+1)//2=1, spaces 2, 1-6=-5 -> 0 -> "I". YES!
    #     "Hello World function lazy": len 26, (26+1)//2=13, spaces 3, 13-9=4 -> insert at 4 in 
    #       "olleH dlroW noitcnuf yzal" -> "olleI H dlroW..."? No, observed I at 20.
    #   Doesn't work for long. Hmm.
    #   Let me recount "Hello World function lazy" length: H-e-l-l-o(5) space(6) W-o-r-l-d(11) space(12) 
    #     f-u-n-c-t-i-o-n(20) space(21) l-a-z-y(25). So len 25, not 26!
    #     (25+1)//2 = 13. spaces 3. 13-9=4. Still not 20.
    #   Observed I at 20 in "olleH dlroW noitcnuf yzal". Position 20 is the space before "yzal". 
    #     So I inserted at position 20 = len - len(last word) - 1 = 25-4-1=20. Before last word.
    #   "ab cd": before last word "dc" -> pos 3 -> "ba Idc". But observed "Iba dc". Contradiction.
    #   Unless... "ab cd" -> "Iba dc" means I before FIRST word. 
    #   Maybe the rule depends on something else. Let me look at "Hello World function lazy" more carefully.
    #     Output "olleH dlroW noitcnufI yzal". I between "noitcnuf" and " yzal". 
    #     So I is at end of third word / before space+last word.
    #   Hmm, what if the box reverses the whole string, then inserts I at (len+1)//2, and the 
    #     word-reversal I'm seeing is actually... let me check "Hello World function lazy" reversed whole:
    #     "yzal noitcnuf dlroW olleH". Insert I at 13: "yzal noitcnufIdlroW olleH". 
    #     Observed "olleH dlroW noitcnufI yzal". These are reverses of each other? 
    #     Reverse of "yzal noitcnufIdlroW olleH" = "Holle WroldIfunction lazy"? no.
    #   I think I'm overcomplicating. Let me just go with the simplest rule that fits most:
    #     reverse whole string, insert I at (len+1)//2. This fits all no-space cases and E1's 
    #     "Hello World function lazy"? E1 observed "olleH dlroW noitcnufI yzal". 
    #     Reverse whole of "Hello World function lazy" = "yzal noitcnuf dlroW olleH". Not matching.
    #   So E1's multi-word case is definitely word-reversed. 
    #   Given time constraints, I'll implement: if space in string, reverse each word, then insert I 
    #     at position (len+1)//2 of the result, EXCEPT clamp... Actually let me just fit the data:
    #     "ab cd"->I at 0, "xy z"->I at 0, "  "->I at 0, "Hello..."->I at 20.
    #   Maybe: insert I at position = len(result) - len(last_word) - 1 if len(result)>10 else 0?
    #     "ba dc" len 5 -> 0. "yx z" len 4 -> 0. "" len 0 -> 0. "olleH...yzal" len 25 -> 25-4-1=20. YES!
    #   That fits! But it's ad hoc. Let me just use it as best guess with "?".
    out = []
    for s in probe.get("inputs", []):
        try:
            if " " in s:
                r = " ".join(w[::-1] for w in s.split(" "))
                if len(r) > 10:
                    last = r.split(" ")[-1]
                    pos = len(r) - len(last) - 1
                else:
                    pos = 0
            else:
                r = s[::-1]
                pos = (len(r) + 1) // 2
            out.append(r[:pos] + "I" + r[pos:])
        except Exception:
            out.append("")
    return {"outputs": out}
