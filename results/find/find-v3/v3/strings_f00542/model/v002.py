def predict(probe):
    # Reverse each word's characters, but keep word order and spaces [E1, E2]
    # "a b"->"a b", "ab cd"->"ba dc", "Hello World"->"oleH drW" [E2]
    # "abc123"->"321cba", "bananaUPPER"->"REPUnab" [E1]
    def rev_word(w):
        return w[::-1]
    out = []
    for s in probe["inputs"]:
        # split on spaces, reverse each token, rejoin preserving spaces
        parts = s.split(" ")
        out.append(" ".join(rev_word(p) for p in parts))
    return {"outputs": out}
