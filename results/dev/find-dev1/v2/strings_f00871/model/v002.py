def predict(probe):
    # f reverses each whitespace-separated word in place, preserving word order,
    # then appends "I" [E1: "hello"->"ollehI", "a b"->"a bI"; E2: "ab cd"->"ba dcI",
    # "one two three"->"eno owt eerhtI", "a b c d"->"a b c dI"]
    # Leading/trailing spaces are stripped [E2: "  spaced  "->"decapsI"]
    # Single chars unchanged, empty -> "I" [E1]
    # Case preserved [E1: "Hello"->"olleHI"; E2: "Ab Cd Ef"->"bA dC fEI"]
    def rev_word(w):
        return w[::-1]
    out = []
    for x in probe["inputs"]:
        words = x.split()
        out.append(" ".join(rev_word(w) for w in words) + "I")
    return {"outputs": out}
