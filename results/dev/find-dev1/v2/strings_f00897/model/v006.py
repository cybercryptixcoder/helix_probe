def predict(probe):
    # Model beliefs:
    # 1) Character-wise cipher, independent per char [E1-E10].
    # 2) Position 0: shift +2 if ord(ch) in [61,86] or [94,118]; else +4 [E1-E10].
    #    - [61,86] = '='..'V'  (includes =,>,?,@,A-Z up to V) [E9,E6]
    #    - [94,118] = '^'..'v' (includes ^,_,`,a-v) [E10,E6,E7]
    #    - everything else ASCII: +4 [E1-E10]
    # 3) Non-ASCII at pos 0: +2 (é->ë) [E4]. Guess same for pos>0 (?) [E4].
    # 4) Position >0: shift +4 for all ASCII [E1-E10].
    #    Non-ASCII at pos>0: guess +2 (?) — no evidence.
    inputs = probe.get("inputs", [])
    outputs = []
    for s in inputs:
        out = []
        for i, ch in enumerate(s):
            o = ord(ch)
            if i == 0:
                if o > 127:
                    shift = 2
                elif 61 <= o <= 86 or 94 <= o <= 118:
                    shift = 2
                else:
                    shift = 4
            else:
                if o > 127:
                    shift = 2  # ?
                else:
                    shift = 4
            out.append(chr(o + shift))
        outputs.append(''.join(out))
    return {"outputs": outputs}
