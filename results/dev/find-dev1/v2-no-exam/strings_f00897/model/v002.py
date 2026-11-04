def predict(probe):
    # Rule: each character is shifted by +2 in ASCII, EXCEPT the first character
    # of the string, which is shifted by +4. [E1, E2]
    #   'a'->'c' (+2)? No: 'a'->'c' is +2... wait.
    # Let's recheck against E2:
    #   'z'->'~' : z=122, ~=126 => +4 (single char, first char)
    #   'Z'->'^' : Z=90, ^=94 => +4
    #   'y'->'}' : y=121, }=125 => +4
    #   '~'->'\x82': ~=126, 130 => +4
    #   '}'->'\x81': }=125, 129 => +4
    #   'ba'->'de': b=98,d=100 (+2); a=97,e=101 (+4)
    #   'aa'->'ce': a=97,c=99 (+2); a=97,e=101 (+4)
    #   'aA'->'cE': a->c (+2); A=65,E=69 (+4)
    #   'A a'->'C$e': A->C (+2); space=32,$=36 (+4); a->e (+4)
    #   'zzz'->'~~~': z=122,~=126 (+4) for ALL three!
    # So: first char +2, subsequent +4. But 'z'->'~' is +4, not +2!
    # And 'a'->'c' is +2. Difference: 'a' is lowercase letter, 'z' is lowercase letter too.
    # Hmm. 'z'->'~' +4 but 'a'->'c' +2. Both lowercase single chars.
    # Wait E1: 'a'->'c' +2, 'A'->'C' +2, '1'->'5' +4, ' '->'$' +4, '!'->'%' +4.
    # E2: 'z'->'~' +4, 'Z'->'^' +4, 'y'->'}' +4.
    # So single 'a','A' +2 but 'z','Z','y' +4? 
    # Maybe it's +2 for first char, but wraps? No.
    # Alternative: shift is +2 for chars in first half of alphabet, +4 for second half?
    # a(97)->c(99) +2; z(122)->~(126) +4. y(121)->}(125) +4.
    # A(65)->C(67) +2; Z(90)->^(94) +4.
    # 'ba': b->d +2, a->e +4. b is first half, a is first half but +4 (position 1).
    # 'aa': a->c +2 (pos0), a->e +4 (pos1).
    # 'zzz': z->~ +4 (pos0!), z->~ +4, z->~ +4.
    # So pos0: 'a' +2, 'z' +4. Hmm.
    # Maybe rule: shift +2 if char code is even? a=97 odd... no.
    # Maybe: shift +2 for chars where (code mod 4) == 1? a=97, 97 mod4=1 ->+2. A=65,65mod4=1->+2. 
    #   z=122,122mod4=2 ->+4. Z=90,90mod4=2->+4. y=121,121mod4=1 -> should be +2 but observed +4!
    # Hmm y=121 mod4=1 but +4. Contradiction.
    # Let's tabulate pos0 results:
    #   a(97)->c(99): +2
    #   A(65)->C(67): +2
    #   1(49)->5(53): +4
    #   space(32)->$(36): +4
    #   !(33)->%(37): +4
    #   z(122)->~(126): +4
    #   Z(90)->^(94): +4
    #   y(121)->}(125): +4
    #   ~(126)->\x82(130): +4
    #   }(125)->\x81(129): +4
    #   b(98)->d(100): +2 (from 'ba')
    #   a(97)->c(99): +2 (from 'aa')
    #   a(97)->c(99): +2 (from 'aA')
    #   A(65)->C(67): +2 (from 'A a')
    #   z(122)->~(126): +4 (from 'zzz')
    # So pos0: a,A,b -> +2; z,Z,y,1,space,!,~,} -> +4.
    # Letters a,b,A +2. Letters z,Z,y +4. Hmm.
    # Maybe: +2 if char is in "aAbB..."? No.
    # Maybe: +2 if char code < some threshold? a=97,b=98,A=65 -> +2. y=121,z=122,Z=90 -> +4.
    #   Threshold between 98 and 121? But Z=90 is +4 while A=65 is +2. So not simple threshold.
    # Maybe: +2 if char is a letter AND in first half of alphabet (a-m, A-M)?
    #   a,b,A yes. y,z,Z no. That fits!
    # Check subsequent chars: all +4 in E1/E2? 
    #   'ab': b->f +4 (b is first half but pos1 -> +4). So pos>=1 always +4.
    #   'zzz': all +4, consistent (pos0 z is second half -> +4).
    # So rule: pos0: if letter in a-m or A-M, +2; else +4. pos>=1: +4.
    # Check E1 'Hello, World!': H(72) is A-M -> +2 -> J. Rest +4. Matches!
    # Check 'a b': a->c +2 (a in a-m), space +4, b +4. Matches.
    # Check 'AB': A->C +2, B->F +4. Matches.
    # Check '12': 1->5 +4, 2->6 +4. Matches.
    # Great, this fits all evidence.
    out = []
    for s in probe.get("inputs", []):
        r = []
        for i, ch in enumerate(s):
            if i == 0 and (('a' <= ch <= 'm') or ('A' <= ch <= 'M')):
                r.append(chr(ord(ch) + 2))
            else:
                r.append(chr(ord(ch) + 4))
        out.append("".join(r))
    return {"outputs": out}
