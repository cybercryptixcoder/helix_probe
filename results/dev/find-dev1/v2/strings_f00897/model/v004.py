def predict(probe):
    # Model of f(x):
    # - Empty string -> empty string [E1]
    # - First character: shift depends on character class [E1,E3,E4,E5,E6]
    #     letters a-u, A-U: +2  [E1,E3,E5,E6]
    #     letters v-z, V-Z: +4  [E5,E6]  (z->~, Z->^, y->}, Y->], x->|, X->\, w->{, W->[, v->x, V->X)
    #     "@": +2  [E3,E4]
    #     digits, space, "!": +4  [E1,E4,E5]
    #     high-ASCII (é): +2  [E4]
    # - Later characters: +4 uniformly [E1,E2,E3,E4]
    results = []
    for s in probe.get("inputs", []):
        r = ""
        for i, ch in enumerate(s):
            if i == 0:
                if ch.isalpha() and ch.lower() in "abcdefghijklmnopqrstu":
                    r += chr(ord(ch) + 2)
                elif ch.isalpha():
                    r += chr(ord(ch) + 4)
                elif ch == "@":
                    r += chr(ord(ch) + 2)
                elif ord(ch) >= 128:
                    r += chr(ord(ch) + 2)
                else:
                    r += chr(ord(ch) + 4)
            else:
                r += chr(ord(ch) + 4)
        results.append(r)
    return {"outputs": results}
