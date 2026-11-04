def predict(probe):
    # Deduplicate characters keeping first occurrence, case-sensitive [E2, E3, E4, E5]
    # Then: if the deduplicated string ends with 'h', do NOT append another 'h' [E6]
    #   "h"->"h", "hh"->"h", "hello h"->"helo " (space kept, h dropped as dup? no...)
    #   Actually: "hello h" -> "helo " : dedup gives "helo h", then trailing 'h' removed? 
    #   Let's re-derive: dedup("hello h") = "helo h" (h,e,l,o,space,h->h dup) = "helo " ... 
    #   Wait: h,e,l,l,o,space,h -> h,e,l,o,space (second h is dup) = "helo " -> yes! "helo "
    #   "abc h" -> dedup = "abc h" -> ends with h, no append -> "abc h" [E6]
    #   "h h" -> dedup = "h " -> ends with space, append h? observed "h " no append...
    #   Hmm "h h" observed "h ". dedup("h h")="h " (h,space,h dup) = "h ". No h appended.
    #   "ha"->"ha", "ah"->"ah", "a h"->"a h", "banana h"->"ban h", "testh"->"tesh"
    #   "banana h": b,a,n,a,n,a,space,h -> b,a,n,space,h = "ban h" ends h, no append -> "ban h" ✓
    #   "testh": t,e,s,t,h -> t,e,s,h = "tesh" ends h, no append -> "tesh" ✓
    #   "ha": h,a -> "ha", doesn't end h, append -> "hah"? but observed "ha"!
    #   So append 'h' only if result does NOT end with 'h' AND ... "ha"->"ha" no append?
    #   Recheck E3: "lazy"->"lazyh", "banana"->"banh", "level"->"levh". These append h.
    #   "ha"->"ha" no append. "ah"->"ah" no append. "a h"->"a h" no append.
    #   Maybe: append h only if input doesn't contain 'h'? "ha" contains h -> no append. 
    #   "ah" contains h -> no append. "a h" contains h -> no append. "testh" contains h -> no append.
    #   "banana h" contains h -> no append. "h h" contains h -> no append. "abc h" contains h -> no append.
    #   "hello h" contains h -> no append -> "helo " ✓
    #   "h"->"h", "hh"->"h" ✓
    #   Check E2: "Hello HELLO" contains h? H uppercase, h lowercase in "Hello". dedup="Helo ELO" 
    #     observed "Helo ELOh" -> appended h! So contains 'h' but appended. Hmm.
    #     Wait "Hello HELLO": H,e,l,l,o,space,H,E,L,L,O -> H,e,l,o,space,E,L,O = "Helo ELO"
    #     observed "Helo ELOh" - appended. But lowercase 'h'? "Hello" has lowercase... no, "Hello" = H-e-l-l-o, no lowercase h. 
    #     So no lowercase 'h' in input -> append. ✓
    #   So rule: append 'h' unless input contains lowercase 'h' [E6]
    #   Check "testh" has lowercase h -> no append -> "tesh" ✓
    #   Check E4 "hello there": has h -> no append -> "helo tr" ✓ (observed "helo tr")
    #   "the quick brown fox": has h -> no append -> "the quickbrownfx" ✓
    #   E5 "function Hello World": f,u,n,c,t,i,o,n,space,H,e,l,l,o,space,W,o,r,l,d
    #     dedup = f,u,n,c,t,i,o,space,H,e,l,W,r,d = "functio HelWrd" no lowercase h -> append -> "functio HelWrdh" ✓
    def transform(s):
        seen = set()
        out = []
        for ch in s:
            if ch in seen:
                continue
            seen.add(ch)
            out.append(ch)
        res = ''.join(out)
        if 'h' not in s:
            res += 'h'
        return res
    return {"outputs": [transform(x) for x in probe["inputs"]]}
