def predict(probe):
    # Beliefs:
    # - Drop every lowercase 'm' from the input, before any case change [E4, E6, E8, E10, E12]
    #   Uppercase 'M' is kept [E4 "EXAMPLE"->"Example", E10 "MUsic"->"Music", E5 "aMiXeD"->"Amixed"]
    # - Then lowercase the whole string [E1, E2]
    # - Then capitalize the first character (no-op if whitespace) [E1, E2, E7, E9]
    #   Leading whitespace thus prevents visible capitalization [E2, E7, E9]
    def f(s):
        s = s.replace('m', '').lower()
        return s[:1].upper() + s[1:] if s else s
    return {"outputs": [f(s) for s in probe["inputs"]]}
