def predict(probe):
    # Model beliefs:
    # 1) Character-wise cipher, independent per char [E1-E13].
    # 2) Position 0: shift +2 if ord(ch) in [61,86] or [94,118], or non-ASCII; else +4 [E1-E13].
    #    - [61,86] = '='..'V' [E9,E6,E13]
    #    - [94,118] = '^'..'v' [E10,E6,E7,E13]
    #    - non-ASCII at pos 0: +2 (é->ë) [E4,E11]
    # 3) Position >0: shift +4 for ALL characters, ASCII and non-ASCII [E1-E13].
    #    - é at pos>0 -> í (+4) [E11]
    # 4) ']' (93) at pos 0 is +4 (-> 'a')? No: E12/E13 show ']-' -> 'y1', i.e. +4? 
    #    ']'=93, 'y'=121, diff=28... wait: 93+4=97='a'. Observed 'y'. So ']' -> +4? No.
    #    Recheck: E12 ']-' -> 'y1'; E13 ']-' -> 'y1'. 93->121 is +28. Hmm.
    #    Actually ']' is 93; 'y' is 121; 121-93=28. That's not +2 or +4.
    #    But E10 ']-' -> 'y1' too. So ']' at pos0 maps to 'y'. 
    #    Wait — maybe I misread. Let me reconsider: perhaps ']' is in a +2 region? 93+2=95='_'. No.
    #    The observed 'y' for ']' is consistent across E10,E12,E13. So ']' -> 'y' (+28).
    #    Hmm, that breaks the simple rule. But maybe it's +4 wrapping? No.
    #    Actually: could the rule be that ']' (93) is +4 giving 'a'? Observed 'y'. So no.
    #    Let me look: E10 inputs include "]-" -> "y1". E12 "]-" -> "y1". E13 "]-" -> "y1".
    #    So ']' at pos0 -> 'y'. That's +28. Odd. But '^' (94) -> 'z' (+2) per E13 "^-"->"z1".
    #    And '[' (91) -> '_' (+4) per E10 "[ -" -> "_$1"? Actually "[ -" -> "_$1": '['->'_' (+4), ' '->'$' (+4). Yes.
    #    So '[' (91) +4, ']' (93) -> 'y'?? That's weird. 
    #    Wait, maybe ']' is being treated as +2 region? 93 is not in [94,118]. 
    #    Hmm, but observed 'y'=121. 93+28. Could there be a different rule for ']'?
    #    Actually maybe I should reconsider: is ']' perhaps +4 but the char after? No, pos0.
    #    Let me just trust: ']' -> 'y'. This is a genuine anomaly. But E10,E12,E13 all agree.
    #    Could it be that ']' maps via +4 to 'a' but then... no.
    #    Actually wait: maybe the region is [94,118] for +2, and ']'=93 is +4 -> 'a'. But observed 'y'.
    #    Unless... the observed for "]-" in E10 is "y1". Hmm 'y' is 121.
    #    I'll treat ']' as a special: 93 -> 121 (+28)? That seems too ad hoc.
    #    Alternative: maybe the rule is +2 for [61,86] and [94,118], and ']'=93 falls in +4 giving 'a',
    #    but the actual observed is 'y'. So maybe the +2 region is [61,86] and [93,118]? 93+2=95='_', not 'y'.
    #    So no. ']' -> 'y' is +28. Strange but consistent. I'll encode it as: ']' at pos0 -> 'y'.
    #    Actually, let me reconsider whether it's +4 with some other base... no.
    #    Given consistency, I'll add: ']' (93) at pos0 shifts +28? That's ugly. 
    #    Hmm, but maybe the real rule: the two +2 intervals are [61,86] and [94,118], and ']'=93 is +4 -> 'a'.
    #    But three experiments say 'y'. So the box does 'y'. I must match the box.
    #    I'll encode ']' -> 'y' as a special case with a comment "?".
    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        out = []
        for i, ch in enumerate(s):
            o = ord(ch)
            if i == 0:
                if o == 93:  # ']' -> 'y' [E10,E12,E13] ?
                    out.append('y')
                    continue
                if o > 127:
                    shift = 2
                elif 61 <= o <= 86 or 94 <= o <= 118:
                    shift = 2
                else:
                    shift = 4
            else:
                shift = 4
            out.append(chr(o + shift))
        outputs.append(''.join(out))
    return {"outputs": outputs}
