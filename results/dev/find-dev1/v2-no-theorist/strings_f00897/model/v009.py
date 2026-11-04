def predict(probe):
    # Position-0 shift rules (evidence):
    # - ASCII 64..87 ('@'..'W') and 95..118 ('_'..'v'): +2 [E6,E7,E10,E11,E12,E13,E14,E15,E16]
    # - ASCII 61,62 ('=','>') and 93,94 (']','^'): +28 [E10,E16]
    # - everything else ASCII: +4 [E1-E16]
    # - non-ASCII (>=128): +2 [E17] (é->ë, à->â, ÿ->ā, É->Ë, À->Â, ß->á, ñ->ó, ø->ú, ¢->¦, £->§)
    #   Note: ¢(0xA2)->¦(0xA6)=+4, £(0xA3)->§(0xA7)=+4. So non-ASCII is NOT uniformly +2!
    #   Re-examine E17: é(0xE9)->ë(0xEB)=+2, à(0xE0)->â(0xE2)=+2, ÿ(0xFF)->ā(0x101)=+2,
    #   É(0xC9)->Ë(0xCB)=+2, À(0xC0)->Â(0xC2)=+2, ß(0xDF)->á(0xE1)=+2, ñ(0xF1)->ó(0xF3)=+2,
    #   ø(0xF8)->ú(0xFA)=+2, ¢(0xA2)->¦(0xA6)=+4, £(0xA3)->§(0xA7)=+4.
    #   So 0xA2,0xA3 -> +4; 0xC0..0xFF -> +2. Band boundary somewhere between 0xA3 and 0xC0.
    #   Guess: non-ASCII +2 band is 0xC0..0xFF (Latin-1 letters), else +4. Marked "?".
    # Position>0: always +4 [E13]
    def shift(ch, pos):
        o = ord(ch)
        if pos == 0:
            if o in (61, 62, 93, 94):
                return chr(o + 28)
            if 64 <= o <= 87 or 95 <= o <= 118:
                return chr(o + 2)
            if 0xC0 <= o <= 0xFF:  # ? non-ASCII Latin-1 letters +2
                return chr(o + 2)
        return chr(o + 4)
    return {"outputs": ["".join(shift(c, i) for i, c in enumerate(s)) for s in probe["inputs"]]}
