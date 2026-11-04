def predict(probe):
    # Model beliefs:
    # 1) Character-wise cipher, independent per char [E1-E11].
    # 2) Position 0: shift +2 if ord(ch) in [61,86] or [94,118], or non-ASCII; else +4 [E1-E11].
    #    - [61,86] = '='..'V' (includes =,>,?,@,A-Z up to V) [E9,E6]
    #    - [94,118] = '^'..'v' (includes ^,_,`,a-v) [E10,E6,E7]
    #    - non-ASCII at pos 0: +2 (é->ë) [E4,E11]
    # 3) Position >0: shift +4 for ALL characters, ASCII and non-ASCII [E1-E11].
    #    - é at pos>0 -> í (+4) [E11]
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
                shift = 4
            out.append(chr(o + shift))
        outputs.append(''.join(out))
    return {"outputs": outputs}
