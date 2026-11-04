def predict(probe):
    # Model: shift each char by +2 if it's in first half of alphabet (a-m/A-M),
    # else +4. Applies to ALL chars uniformly (letters, digits, spaces, symbols).
    # Evidence:
    # - E1: "abc123"->"cfg567": a+2,b+2,c+2, 1+4,2+4,3+4 (digits +4)
    # - E1: "level"->"nizip": l+2,e+4,v+4,e+4,l+4 (only first char is a-m)
    # - E1: " Zebralower"->"$^ifveps{iv": space+4, Z+4, e+4,b+4,r+4,a+4,l+4,o+4,w+4,e+4,r+4
    # - E1: "Hello World function lazy"->"Jipps$[svph$jyrgxmsr$pe~}": H+2,e+4,l+4,l+4,o+4, space+4, W+4,o+4,r+4,l+4,d+4, space+4, f+4,u+4,n+4,c+4,t+4,i+4,o+4,n+4, space+4, l+4,a+4,z+4,y+4
    # - E1: "bananaUPPER"->"derereYTTIV": b+2,a+4,n+4,a+4,n+4,a+4, U+4,P+4,P+4,E+4,R+4
    # - E1: "Zebra"->"^ifve": Z+4,e+4,b+4,r+4,a+4
    # - E2: "nop"->"pst": n+2,o+4,p+4 (n is NOT first half, yet +2!)
    #   Wait: n is 14th letter, second half. But output p = n+2. So rule is NOT first-half.
    #   Re-examine: "mno"->"ors": m+2,n+4,o+4. m is first half, +2. 
    #   "nop"->"pst": n+2. n is second half but +2. Contradiction with first-half rule.
    #   "aop"->"cst": a+2. "zop"->"~st": z+2. "0op"->"4st": 0+4. " op"->"$st": space+4.
    #   So first char: letters always +2 (a..z, A..Z), non-letters +4.
    #   Check E1: "abc123": a+2 yes. "level": l+2 yes. " Zebralower": space+4 yes.
    #   "Hello...": H+2 yes. "bananaUPPER": b+2 yes. "Zebra": Z+2? But observed "^ifve" = Z+4!
    #   Z is a letter but got +4. Hmm. "Zebra"->"^ifve": ^ is Z+4. Contradiction.
    #   Wait E2 "Zop"->"^st": Z+4. So uppercase Z gets +4, but lowercase z gets +2 ("zop"->"~st").
    #   And "NOP"->"PST": N+2. "MNO"->"ORS": M+2. "AOP"->"CST": A+2.
    #   So uppercase letters: A..? +2, Z +4. Lowercase: a..z all +2.
    #   Check E1 "Zebra": Z+4 consistent. "Hello": H+2. "bananaUPPER": b+2.
    #   What about uppercase range? A+2 (E2), M+2, N+2, Z+4. Maybe uppercase only A-Y +2, Z+4? 
    #   Or maybe uppercase +2 except Z? Need more data but best guess: uppercase A-Y +2, Z+4.
    #   Actually reconsider: maybe rule is "letter that is not the last letter of its case"? 
    #   Lowercase z+2 though. So asymmetric. 
    #   Alternative: maybe it's based on ord+2 being a letter? Z+2='\\' not letter -> +4. 
    #   z+2='|' not letter but got +2. So no.
    #   Let's just encode: first char letter (a-z or A-Y) -> +2, else +4. Z -> +4.
    #   Hmm but is it really Z specifically? Could be uppercase second-half? N+2 rules that out.
    #   Could be "Z" only. Mark with ?.
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, c in enumerate(s):
            if i == 0:
                if ('a' <= c <= 'z') or ('A' <= c <= 'Y'):
                    sh = 2
                else:
                    sh = 4
            else:
                sh = 4
            try:
                r.append(chr(ord(c) + sh))
            except (ValueError, OverflowError):
                r.append(c)
        out.append("".join(r))
    return {"outputs": out}
