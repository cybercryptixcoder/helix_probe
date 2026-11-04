def predict(probe):
    # Position-0 shift: +2 for codepoints in {58..62} ∪ {64..87} ∪ {91..94} ∪ {95..118}; else +4.
    #   E14: ':'(58)->'>'(+4)? no: E16 ':'->'>' is +4. Wait: E16 ':'->'>' = +4. ';'(59)->'?'(+4). '<'(60)->'@'(+4). '='(61)->'Y'(+4)? '='->'Y' is +23?? 
    # Re-examine E16: ';'->'?'(+4), '<'->'@'(+4), '='->'Y'(+23)?? '>'->'Z'(+22)??
    # Actually E16 observed: ["_","`","y","z","?","@","Y","Z",">","A"] for ["[","\\","]","^",";","<","=",">",":","?"]
    #   '['(91)->'_'(+4), '\\'(92)->'`'(+4), ']'(93)->'y'(+24)??, '^'(94)->'z'(+26)??
    #   ';'(59)->'?'(+4), '<'(60)->'@'(+4), '='(61)->'Y'(+24)?, '>'(62)->'Z'(+24)?
    #   ':'(58)->'>'(+4), '?'(63)->'A'(+4)
    # Hmm ']'->'y' and '^'->'z' and '='->'Y' and '>'->'Z' are weird. Compare E10: ']'->'y', '^'->'z', '='->'Y', '>'->'Z'. Same!
    # So these are consistent. What's the rule? ']'(93)->'y'(121): +28. '^'(94)->'z'(122): +28. '='(61)->'Y'(89): +28. '>'(62)->'Z'(90): +28.
    # Interesting: +28 for these. And '['(91)->'_'(95): +4. '\\'(92)->'`'(96): +4.
    # Maybe: chars in 91..94 map to 95..98? No, ']'->'y'. 
    # Alternative: these chars map via some class transform. ']'->'y'? '^'->'z'? 
    # Maybe the rule is: shift by +4, but if result would be in some range, add more? ']'+4='a'(97), but observed 'y'(121). 
    # Or: '='->'Y': '=' is 61, 'Y' is 89. 61+28=89. '>'+28=90='Z'. ']'+28=121='y'. '^'+28=122='z'.
    # What do 61,62,93,94 have in common? They're the "high" ends of punctuation runs? 
    # 61,62 = '=','>' ; 93,94 = ']','^'. Hmm.
    # Maybe map to uppercase/lowercase by position in a class. '=' and '>' are the last two of <=>? 
    # Actually: maybe the box maps certain punctuation to letters. ']'->'y', '^'->'z' (last two lowercase). '='->'Y', '>'->'Z' (last two uppercase).
    # So '=' and '>' -> 'Y','Z' (uppercase tail); ']' and '^' -> 'y','z' (lowercase tail).
    # And '['->'_', '\\'->'`' (+4). ';'->'?', '<'->'@' (+4). ':'->'>' (+4). '?'->'A' (+4).
    # This is getting complex. Let me reconsider: maybe there's a "wrap" or class-based mapping.
    # Simplest consistent rule: position 0 shifts +4 normally, EXCEPT a +2 band {64..87}∪{95..118}, AND special mappings for {61,62,93,94} -> {89,90,121,122}.
    # But that's ad hoc. Let me check: is 61->89 = 61+28, 62->90=+28, 93->121=+28, 94->122=+28. All +28!
    # And 91->95=+4, 92->96=+4. 59->63=+4, 60->64=+4. 58->62=+4. 63->67=+4.
    # So {61,62,93,94} shift +28, others in punctuation shift +4.
    # What's special about 61,62,93,94? 61='=',62='>',93=']',94='^'. 
    # Hmm, 61,62 are the top of 58-62; 93,94 are the top of 91-94. So the LAST TWO of each punctuation run shift +28?
    # 58,59,60 shift +4; 61,62 shift +28. 91,92 shift +4; 93,94 shift +28.
    # That's a pattern! Last two of a run of 5 (58-62) and last two of a run of 4 (91-94).
    # But why +28? 61+28=89='Y', 62+28=90='Z'. 93+28=121='y', 94+28=122='z'.
    # Maybe the rule: these map to the last chars of letter classes. '='->'Y', '>'->'Z' (uppercase); ']'->'y', '^'->'z' (lowercase).
    # This is a "class-based" mapping: certain punctuation maps to letter-class tails.
    # I'll encode: pos0, if o in {61,62}: chr(o+28); if o in {93,94}: chr(o+28); elif 64<=o<=87 or 95<=o<=118: +2; else +4.
    # Check E10: 'O'(79)->'Q'(+2) ok. E14: ':'(58)->'>'(+4) ok, '?'(63)->'A'(+4) ok, '@'(64)->'B'(+2) ok.
    # E12: '?'->'A'(+4), '@'->'B'(+2), 'A'->'C', 'Z'->'^'(+4), '['->'_'(+4), '`'->'b'(+2), 'a'->'c', 'v'->'x', 'w'->'{'(+4), '{'->\x7f(+4). All ok.
    # E15: 'X'->'\\'(+4), 'Y'->']'(+4), '^'->'z'(+28) ✓, '_'->'a'(+2), 'w'->'{'(+4), 'x'->'|'(+4), '?'->'A'(+4), '@'->'B'(+2), '`'->'b'(+2), '{'->\x7f(+4). All ok!
    # E16: '['->'_'(+4), '\\'->'`'(+4), ']'->'y'(+28)✓, '^'->'z'(+28)✓, ';'->'?'(+4), '<'->'@'(+4), '='->'Y'(+28)✓, '>'->'Z'(+28)✓, ':'->'>'(+4), '?'->'A'(+4). All ok!
    # E11: P..W +2, X->\\ (+4), Y->] (+4). ok.
    # E7: u,v +2, w..z +4. ok.
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0:
            if o in (61, 62, 93, 94):
                return chr(o + 28)
            if 64 <= o <= 87 or 95 <= o <= 118:
                return chr(o + 2)
        return chr(o + 4)
    return {"outputs": ["".join(shift(c, i) for i, c in enumerate(s)) for s in probe["inputs"]]}
