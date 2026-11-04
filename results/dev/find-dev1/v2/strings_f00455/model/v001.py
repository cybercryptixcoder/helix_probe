def predict(probe):
    # Each character's code point is increased by 1 [E1: a->B, A->B, 1->2, !->", space->!, ab->Bc, Hello->Ifmmp, hello world->Ifmmp!xpsme, 123->234]
    # Empty string stays empty [E1]
    def shift(s):
        return ''.join(chr(ord(c) + 1) for c in s)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
