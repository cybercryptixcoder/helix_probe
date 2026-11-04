def predict(probe):
    # Insert 'Z' after each 'a' (lowercase a) [E1: abc123->abcZ123, level->leZvel, Zebralower->ZebraZlower, bananaUPPER->bananZaUPPER, Zebra->ZeZbra]
    # Spaces are removed [E1: "Hello World function lazy"->"HelloWorldfZunctionlazy", " Zebralower"->"ZebraZlower"]
    # Note: 'f' in "function" became "fZunction" — wait, that's 'u'? No: "function"->"fZunction" means 'u' got Z? Let's recheck.
    # Actually "function" -> "fZunction": the Z is after 'f', before 'u'. Hmm, but rule says after 'a'. Let's recheck all.
    # abc123->abcZ123: Z after c? No, after 'c'? abc -> abcZ. That's after 'c', not 'a'. Wait 'a' is first char.
    # Hmm. Let's look: "abc123" -> "abcZ123". Z inserted after 'c'.
    # "level" -> "leZvel": after 'e'.
    # "Zebralower" -> "ZebraZlower": after 'a' (the 'a' in Zebra).
    # "bananaUPPER" -> "bananZaUPPER": after 'a' (last a).
    # "Zebra" -> "ZeZbra": after 'e'.
    # "Hello World function lazy" -> "HelloWorldfZunctionlazy": after 'f'.
    # So Z is inserted after the 2nd character? abc->abcZ no. Let's count positions.
    # abc123: insert after index 2 (0-based) = 'c'. level: after index 1 = 'e'. Zebralower: after index 4='a'. bananaUPPER: after index 4='a'? banana = b a n a n a, index4='n'. Hmm.
    # Let's find: maybe after the 2nd vowel? abc: vowels a -> after a? no.
    # Try: insert Z after the letter that is... let's list inserted position (char before Z):
    # abc123: 'c'
    # level: 'e' (index1)
    # Zebralower: 'a' (index4)
    # bananaUPPER: 'a' (index4? banana indices: b0 a1 n2 a3 n4 a5; Z after index4='n'? output bananZa: b a n a n Z a -> Z after index4 'n'. yes 'n')
    # Zebra: 'e' (index1)
    # HelloWorldfunctionlazy: 'f' in function. Full: HelloWorldfunctionlazy. After removing spaces: HelloWorldfunctionlazy. Z after 'f' which is at... H e l l o W o r l d f u n c t i o n l a z y. f at index10.
    # Hmm inconsistent. Maybe it's after the 2nd occurrence of something? Or after a specific letter pattern.
    # Let's check: maybe insert Z after the 2nd character from... no.
    # Maybe after the letter that is alphabetically... 
    # abc123: c (3rd). level: e (2nd). Zebralower: a (5th). bananaUPPER: n (5th). Zebra: e (2nd). function: f (11th).
    # Maybe after the 2nd vowel? abc: a is 1st vowel, then... only one vowel. Hmm.
    # Maybe after the letter 'e' or 'a' or 'c' or 'n' or 'f'... 
    # Try: after the 2nd distinct... 
    # Wait — maybe it's after the letter that comes right before a repeated letter? level: 'e' before 'v'? no.
    # Let's think differently: maybe Z inserted after the 2nd character of each word? abc123 word1: after 2nd char 'b'? no, after 'c'.
    # Hmm, "Hello World function lazy" -> spaces removed AND Z inserted. Maybe Z inserted after 2nd char of the whole string after space removal? HelloWorld... 2nd char 'e' -> HeZllo? no, output HelloWorldfZunctionlazy.
    # Let's reconsider: maybe the rule is insert Z after the 2nd occurrence of a vowel? 
    # abc123: vowels a -> only 1. no.
    # Maybe after the letter at position = length/2? abc123 len6, pos3='1'? no.
    # Let me look at "Zebralower"->"ZebraZlower": Z after 'a' at index4. len=10, mid=5. no.
    # Maybe after the 2nd 'a'? Zebralower has a at index4 only. bananaUPPER has a at 1,3,5. Z after index4 'n'? that's after 2nd 'a'? 2nd a is index3, next char index4='n'. So Z after the char following 2nd 'a'? For Zebralower, 2nd a doesn't exist.
    # Hmm. Let's try: insert Z after the 2nd letter that is... 
    # abc123: letters a,b,c. 2nd letter b -> abZc? no.
    # Maybe after the letter 'c','e','a','n','f' — these are all... 3rd,5th,1st,14th,6th letters. no.
    # Let's try: after the 2nd consonant? abc: consonants b,c. 2nd consonant c -> abcZ. yes! level: consonants l,v,l. 2nd consonant v -> levZel? no, output leZvel (Z after e, before v).
    # Hmm leZvel: Z after 'e' which is 1st vowel. 
    # Maybe after the 2nd vowel? level: vowels e,e. 2nd vowel is index3 'e'? le v e l: e0? l0 e1 v2 e3 l4. 2nd vowel e3 -> lev e Z l = leveZl? no.
    # I'm overcomplicating. Let me just note the observed insertions and see if there's a simpler pattern I'm missing.
    # abc123 -> abcZ123 (Z at index 3)
    # level -> leZvel (Z at index 2)
    # Zebralower -> ZebraZlower (Z at index 5)
    # bananaUPPER -> bananZaUPPER (Z at index 5)
    # Zebra -> ZeZbra (Z at index 2)
    # HelloWorldfunctionlazy -> HelloWorldfZunctionlazy (Z at index 11)
    # Hmm, maybe Z inserted after the 2nd character that is a letter with... 
    # Actually maybe it's after the 2nd occurrence of the letter that appears... no.
    # Let me try: after the 2nd character counting only from a certain set.
    # Or: the box inserts Z after the 2nd letter of the alphabetically... 
    # abc: a,b,c. Z after c (3rd). level: l,e,v,e,l. Z after e (2nd). Zebralower: Z,e,b,r,a,l,o,w,e,r. Z after a (5th). 
    # Maybe after the 2nd vowel counting y? abc: a (1 vowel). no.
    # Maybe after the letter that is the 2nd most common? 
    # I'll go with: insert Z after the 2nd character of the string if... no.
    # Given uncertainty, let me just implement: remove spaces, and insert Z after the 2nd character? abc123 -> abZc123 no.
    # Let me try: insert Z after the 2nd letter (alphabetic char)? abc123: 2nd letter b -> abZc123 no.
    # Hmm what if it's after the 2nd character that is NOT... 
    # abc123: chars a,b,c,1,2,3. Z after c (3rd char). level: l,e,v,e,l. Z after e (2nd char). 
    # Zebralower: Z,e,b,r,a,l,o,w,e,r. Z after a (5th char). 
    # bananaUPPER: b,a,n,a,n,a,U,P,P,E,R. Z after n (5th char). 
    # Zebra: Z,e,b,r,a. Z after e (2nd char).
    # HelloWorldfunctionlazy: H,e,l,l,o,W,o,r,l,d,f,u,... Z after f (11th char).
    # Positions: 3,2,5,5,2,11. Lengths: 6,5,10,11,5,23.
    # 3 vs 6: half. 2 vs 5: ~half. 5 vs 10: half. 5 vs 11: ~half. 2 vs 5: ~half. 11 vs 23: ~half.
    # So Z inserted at the middle! floor(len/2) or ceil.
    # abc123 len6: mid index 3 (0-based) = 'c'? Wait if Z is at index 3, that means inserted before index 3, i.e., after index 2 'c'. len6, index3 = len/2. Yes!
    # level len5: Z at index 2 = floor(5/2)=2. Yes!
    # Zebralower len10: Z at index5 = 10/2. Yes!
    # bananaUPPER len11: Z at index5 = floor(11/2)=5. Yes!
    # Zebra len5: Z at index2. Yes!
    # HelloWorldfunctionlazy: after space removal len? "HelloWorldfunctionlazy" = 5+5+8+4=22. Z at index 11 = 22/2. Yes!
    # So: remove spaces, then insert 'Z' at the middle (index len//2).
    s = probe["inputs"]
    out = []
    for x in s:
        t = x.replace(" ", "")
        m = len(t) // 2
        out.append(t[:m] + "Z" + t[m:])
    return {"outputs": out}
