def predict(probe):
    # Mechanism: a character substitution applied to uppercase letters only.
    # Uppercase 'B' is deleted (maps to empty); uppercase 'D' maps to 'J';
    # every other character is unchanged.
    # Evidence:
    #  B deleted: ABC123->AC123 [E12], AB123->A123, A1B2->A12, ABC-123->AC-123,
    #             ABC 123->AC 123, ABCD123->ACJ123, AB12CD34->A12CJ34, x ABC123 y->x AC123 y [E13]
    #  D->J:      abcDEF123->abcJEF123, DEF123abc->JEF123abc, ABCD123->ACJ123,
    #             AB12CD34->A12CJ34 [E13]
    #  Lowercase b,d unchanged: abc123 [E12], Order #42 shipped. [E4], a=1&b=2 [E7]
    #  Other uppercase seen unchanged: A,C,E,F,H,L,O,W [E1,E6,E12,E13]
    #  Other uppercase letters: assumed identity (?) — only B and D observed to change.
    out = []
    for s in probe["inputs"]:
        out.append(s.replace('B', '').replace('D', 'J'))
    return {"outputs": out}
