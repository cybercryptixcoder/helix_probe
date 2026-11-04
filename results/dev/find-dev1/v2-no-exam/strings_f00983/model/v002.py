def predict(probe):
    # Every character's code point is shifted +8, with NO wraparound at 128 [E1, E2]
    # (E2: z->\u0082, ~->\u0086, \u007f->\u0087 — all exceed 127, so no mod 128)
    # Letters/digits/punct all follow plain ord(c)+8 [E1, E2]
    def shift(s):
        return ''.join(chr(ord(c) + 8) for c in s)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
