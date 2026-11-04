def predict(probe):
    # Lowercase letters shift +8: a->i, b->j, c->k [E1]
    # Uppercase letters shift +8: A->I, B->J, C->K [E1]
    # Digits shift +8 with wrap: 1->9, 2->:, 3->; (ASCII +8) [E1]
    # Punctuation shifts +8 in ASCII: !->), space->( [E1]
    # Every character is shifted by +8 in ASCII code [E1]
    def shift(s):
        return ''.join(chr((ord(c) + 8) % 128) for c in s)
    return {"outputs": [shift(x) for x in probe["inputs"]]}
