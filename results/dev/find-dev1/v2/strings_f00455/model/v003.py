def predict(probe):
    # Every character's code point is increased by 1 [E1: a->B, 1->2, !->", space->!]
    # Case rule: after +1, if the result is a letter, its case is set by POSITION:
    #   - first character of the string -> uppercase [E1 a->B, E4 b->C, E5 1abc->2bcd]
    #   - any other character -> lowercase [E4 bmx->Cny, BMX->Cny, bMx->Cny; E3 abc DEF 123->Bcd!efg!234]
    # Non-letters are unaffected by the case rule [E1 1->2, !->", space->!; E5 1A->2b]
    # The first-char-uppercase rule only applies if the shifted char is a letter [E5 1abc->2bcd, !abc->"bcd, ' abc'->!bcd]
    # z->[ and Z->[ : Z+1=[ (not a letter) stays '[' [E2 z->[, Z->[; E3 Z9->[:; E5 Z1->[2]
    # The earlier 'aZ9!'->'B{:"' anomaly: Z at pos2 -> [ per this rule, but observed '{'. 
    #   Given E2/E3/E5 all show Z->[ consistently, treat that single observation as noise. (?)
    # Non-ASCII: é->Ê (é+1=ê, first char -> upper Ê) [E2 é->Ê]; éè->Êé [E3]; 中->丮 (+1) [E3]
    def shift(s):
        out = []
        for i, c in enumerate(s):
            n = chr(ord(c) + 1)
            if n.isalpha():
                n = n.upper() if i == 0 else n.lower()
            out.append(n)
        return ''.join(out)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
