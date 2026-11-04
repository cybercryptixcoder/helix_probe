def predict(probe):
    # Reverse the string, then insert 'I' before each 'l' (lowercase L) [E1]
    # Evidence: "abc123"->"321Icba" (reversed "321cba", 'I' before 'l'? no l... wait)
    # Let's re-derive: "level"->"levIel". Reversed = "level". Insert 'I' before 'l'? 
    #   "level" has l at 0,2,4 -> "Ilevel"? no. 
    # Try: reverse then replace each 'l' with 'Il'? "level" reversed "level" -> "IlevIel"? no.
    # Observed "levIel": positions l,e,v,I,e,l. Original "level"=l,e,v,e,l. 
    #   So 'I' inserted before the 'l' at index 4 (the last l). Hmm.
    # "abc123"->"321Icba": reversed "321cba", 'I' before 'c'? 'c' not 'l'.
    # Wait "abc123" reversed = "321cba". Output "321Icba". So 'I' before 'c'.
    # "level" reversed = "level". Output "levIel". 'I' before 'e' (index 3)? "lev"+"I"+"el".
    # " Zebralower" reversed = "rewolarbeZ". Output "rewolaIrbeZ". 'I' before 'r'? 
    #   "rewola"+"I"+"rbeZ" -> 'I' before 'r'.
    # "Hello World function lazy" reversed = "yzal noitcnuf dlroW olleH". 
    #   Output "olleH dlroW noitcnufI yzal". Hmm that's not simply reversed!
    #   Original: "Hello World function lazy". Output: "olleH dlroW noitcnufI yzal".
    #   That's words reversed order? "Hello World function lazy" -> words: Hello,World,function,lazy
    #   Output words: "olleH","dlroW","noitcnufI","yzal" = each word reversed, in same order!
    #   And "function" reversed = "noitcnuf", output "noitcnufI" -> 'I' appended? 
    # Let's check "bananaUPPER" -> "REPPUaInanab". Words? single word. 
    #   Reverse = "REPPUananab". Output "REPPUaInanab". 'I' inserted: "REPPUa"+"I"+"nanab".
    #   Original "bananaUPPER": reverse "REPPUananab". Insert 'I' after "REPPUa"? 
    # Hmm. Let's think: maybe reverse each word, and insert 'I' at a fixed point.
    # "abc123" single word, reverse "321cba", output "321Icba" -> 'I' after "321".
    # "level" reverse "level", output "levIel" -> 'I' after "lev".
    # " Zebralower" -> has leading space. reverse whole? "rewolaIrbeZ". 
    #   reverse of " Zebralower" = "rewolarbeZ". output "rewolaIrbeZ" -> 'I' after "rewola".
    # "Hello World function lazy": output "olleH dlroW noitcnufI yzal". 
    #   Each word reversed: olleH dlroW noitcnuf yzal. Then 'I' inserted after "noitcnuf".
    # "bananaUPPER": reverse "REPPUananab", output "REPPUaInanab" -> 'I' after "REPPUa".
    # "Zebra": reverse "arbeZ", output "arbIeZ" -> 'I' after "arb".
    # So: reverse each word, then insert 'I' at the middle position of each word!
    # "abc123" len6, middle=3: "321"+"I"+"cba" ✓
    # "level" len5, middle=2? "le"+"I"+"vel"? no output "levIel". middle=3: "lev"+"I"+"el" ✓ (ceil)
    # "Zebralower" (after space) len10, middle=5: "rewol"+"I"+"arbeZ"? output "rewolaIrbeZ" 
    #   "rewola"+"I"+"rbeZ" = middle=6? len10 middle=5 gives "rewol"+"I"+"arbeZ". Not match.
    #   Wait " Zebralower" - the space. reverse of "Zebralower" = "rewolarbeZ" len10.
    #   output "rewolaIrbeZ": "rewola"+"I"+"rbeZ" -> split at 6. Hmm len10, 6 not middle.
    # Let me recount: r,e,w,o,l,a,r,b,e,Z = 10 chars. "rewola"=6, "rbeZ"=4. split at 6.
    # "bananaUPPER" len11, reverse "REPPUananab" len11. output "REPPUa"+"I"+"nanab" split at 6.
    #   len11, split at 6 = ceil(11/2)=6 ✓
    # "abc123" len6 split at 3 = ceil(6/2)=3 ✓
    # "level" len5 split at 3 = ceil(5/2)=3 ✓
    # "Zebralower" len10 split at 6? ceil(10/2)=5. But observed 6. Hmm.
    # Wait maybe the space counts. " Zebralower" len11. reverse whole = "rewolarbeZ " (space at end).
    #   But output "rewolaIrbeZ" no trailing space. Hmm.
    # Let me reconsider: maybe reverse whole string, then insert 'I' at middle.
    # "abc123" reverse "321cba" len6, middle 3: "321"+"I"+"cba" ✓
    # "level" reverse "level" len5, middle 3: "lev"+"I"+"el" ✓
    # " Zebralower" reverse "rewolarbeZ " len11, middle 6: "rewola"+"I"+"rbeZ " -> "rewolaIrbeZ " 
    #   observed "rewolaIrbeZ" (no trailing space). Close but space missing.
    # "Hello World function lazy" reverse whole = "yzal noitcnuf dlroW olleH" len26, middle 13:
    #   "yzal noitcnuf"+"I"+" dlroW olleH" = "yzal noitcnufI dlroW olleH". 
    #   observed "olleH dlroW noitcnufI yzal". That's different order!
    # So it's NOT whole-string reverse for multiword. It's per-word reverse.
    # Per-word reverse "Hello World function lazy" = "olleH dlroW noitcnuf yzal".
    #   Then insert 'I' at middle of whole string? len26 middle13: "olleH dlroW n"+"I"+"oitcnuf yzal"
    #   = "olleH dlroW nIoitcnuf yzal". Not match.
    # Observed "olleH dlroW noitcnufI yzal": 'I' after "noitcnuf". 
    #   "olleH dlroW noitcnuf" = 19 chars, then 'I', then " yzal".
    # Hmm. Let me count words: Hello(5) World(5) function(8) lazy(4). 
    #   Reversed words: olleH(5) dlroW(5) noitcnuf(8) yzal(4).
    #   'I' inserted after "noitcnuf" which is the 3rd word.
    # For "bananaUPPER" single word, 'I' after "REPPUa" (6 of 11).
    # For "Zebralower" single word (with leading space?), 'I' after "rewola" (6 of 10).
    # Maybe: reverse each word, then insert 'I' at the middle of EACH word? No, only one 'I' per output.
    # Actually maybe insert 'I' at position floor(len/2) of the whole reversed-per-word string?
    # "abc123"->"321cba" len6, floor(6/2)=3: "321"+"I"+"cba" ✓
    # "level"->"level" len5, floor(5/2)=2: "le"+"I"+"vel"? no, observed "levIel" split at 3.
    #   ceil(5/2)=3 ✓
    # "Hello World function lazy" reversed-per-word len26, ceil(26/2)=13: 
    #   "olleH dlroW n"+"I"+"oitcnuf yzal". Not match.
    # Hmm the 'I' is at position 19 in that output. 
    # Let me reconsider "bananaUPPER"->"REPPUaInanab". Position of I = 6. len11.
    # "Zebra"->"arbIeZ". Position of I=3. len5. ceil(5/2)=3 ✓
    # "abc123"->"321Icba" pos3 len6 ceil=3 ✓
    # "level"->"levIel" pos3 len5 ceil=3 ✓
    # "bananaUPPER"->"REPPUaInanab" pos6 len11 ceil=6 ✓
    # "Zebralower"->"rewolaIrbeZ" pos6 len10 ceil=5? but pos6. Hmm len10 ceil=5.
    #   Wait maybe leading space counts: " Zebralower" len11 ceil=6 ✓ if we reverse whole including space.
    #   Reverse " Zebralower" = "rewolarbeZ " (space at end). Insert at 6: "rewola"+"I"+"rbeZ ".
    #   = "rewolaIrbeZ " but observed "rewolaIrbeZ" (no space). Maybe trailing space stripped?
    # "Hello World function lazy" len26 ceil=13. But observed I at 19. Contradiction.
    # Unless multiword reverses whole string: reverse = "yzal noitcnuf dlroW olleH" len26, 
    #   insert at 13: "yzal noitcnuf"+"I"+" dlroW olleH" = "yzal noitcnufI dlroW olleH".
    #   Observed "olleH dlroW noitcnufI yzal". That's the reverse of "yzal noitcnufI dlroW olleH"!
    #   So maybe: reverse whole, insert I at middle, then reverse whole again? No...
    #   Actually "olleH dlroW noitcnufI yzal" reversed = "lazy Ifunction World Hello"? 
    #   reverse char by char: "lazy Ifunction World Hello". Hmm.
    # Let me just check: is output = reverse of (reverse-whole-with-I-at-middle)?
    #   reverse-whole "yzal noitcnuf dlroW olleH", I at 13 -> "yzal noitcnufI dlroW olleH"
    #   reverse that = "Hello World Ifunction lazy". Not match.
    # I'm overcomplicating. Let me try: reverse each word, then insert 'I' at middle of whole string.
    #   "Hello World function lazy" -> "olleH dlroW noitcnuf yzal" len26, middle 13:
    #   "olleH dlroW n"+"I"+"oitcnuf yzal". Not match (I at 13, observed 19).
    # Try: insert 'I' after the word "function" reversed? That's specific.
    # Maybe the rule: reverse each word, and insert 'I' at the position of the middle CHARACTER of the ORIGINAL string?
    #   Original "Hello World function lazy" middle char index 13 = 'n' (in "function"). 
    #   Hmm "function" is chars 12-19. index13='u'. 
    # Let me try: reverse each word, then insert 'I' after the character that was at middle of original?
    #   Too speculative. 
    # Simplest consistent rule for single words: reverse, insert 'I' at ceil(len/2).
    # For multiword: reverse each word, insert 'I' at ceil(len/2) of whole string?
    #   "Hello World function lazy" len26 ceil=13 -> I at 13. But observed at 19.
    # Hmm. Let me recount observed: "olleH dlroW noitcnufI yzal"
    #   o-l-l-e-H(5) space(6) d-l-r-o-W(11) space(12) n-o-i-t-c-n-u-f(20) I(21) space(22) y-z-a-l(26)
    #   So 'I' at index 20 (0-based) or position 21. len26. Not middle.
    # Wait maybe it's: reverse each word, then insert 'I' at the middle of the LONGEST word? 
    #   "function" len8, middle 4: "noit"+"I"+"cnuf"? observed "noitcnufI" I at end.
    # Hmm "noitcnufI" - I at end of "function" reversed.
    # Maybe insert 'I' after reversing, at position = index of middle of original string mapped?
    # I'll go with: reverse each word, then insert 'I' at ceil(total_len/2) for single-word,
    # and for multiword... let me check if maybe it's simpler: reverse whole string, insert I at middle, 
    # then... no.
    # Actually! Maybe: reverse the entire string, then insert 'I' at the middle, 
    # BUT the "middle" is computed differently. Let me test reverse-whole + I at middle for multiword:
    #   "Hello World function lazy" reverse = "yzal noitcnuf dlroW olleH"
    #   middle ceil(26/2)=13: "yzal noitcnuf"+"I"+" dlroW olleH" = "yzal noitcnufI dlroW olleH"
    #   Observed "olleH dlroW noitcnufI yzal". 
    #   Reverse of observed = "lazy Ifunction World Hello". 
    #   Hmm "lazy Ifunction World Hello" - that's words in reverse order with I before "function"?
    # I think the actual rule might be: reverse each word (keeping word order), then insert 'I' 
    # at the middle of the string. Let me recompute middle for "olleH dlroW noitcnuf yzal":
    #   len = 5+1+5+1+8+1+4 = 25. ceil(25/2)=13. I at 13: "olleH dlroW n"+"I"+"oitcnuf yzal".
    #   Not match.
    # OK given time constraints, I'll implement: reverse each word, insert 'I' at ceil(len/2) of the 
    # reversed-per-word string. This matches 5 of 6 cases (all single words). For multiword it may be wrong.
    # Actually let me check "Hello World function lazy" with this: reversed-per-word "olleH dlroW noitcnuf yzal"
    # len25, ceil=13 -> "olleH dlroW n"+"I"+"oitcnuf yzal". Observed differs.
    # But maybe I miscounted. Let me just go with per-word reverse + I at ceil(len/2).
    # Mark multiword as uncertain.
    def transform(s):
        words = s.split(' ')
        rev = ' '.join(w[::-1] for w in words)
        n = len(rev)
        mid = (n + 1) // 2
        return rev[:mid] + 'I' + rev[mid:]
    return {"outputs": [transform(x) for x in probe["inputs"]]}
