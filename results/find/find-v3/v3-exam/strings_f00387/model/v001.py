def predict(probe):
    # Hypothesis: capitalize first letter of each word, lowercase the rest.
    # Evidence E1: "abc123"->"Abc123", "level"->"Level", " Zebralower"->" zebralower",
    #   "Hello World function lazy"->"Hello world function lazy",
    #   "bananaUPPER"->"Bananaupper", "Zebra"->"Zebra".
    # This is str.title()? No: title would give "Abc123" ok, but "Bananaupper" ok,
    #   "Hello World..." -> title gives "Hello World Function Lazy" (wrong).
    # It's capitalize-each-word: first char upper, rest lower, per whitespace-separated word.
    # " Zebralower" -> leading space preserved, "zebralower"->"zebralower"? observed " zebralower"
    #   first char after space is 'Z' already upper, rest lower -> "zebralower". Yes.
    # "abc123" -> "Abc123": first char 'a'->'A', rest lower. Yes.
    def cap_word(w):
        if not w:
            return w
        return w[0].upper() + w[1:].lower()
    out = []
    for s in probe["inputs"]:
        # split on whitespace but keep it: use re to split into word/non-word runs
        import re
        parts = re.split(r'(\s+)', s)
        out.append(''.join(p if p.isspace() or p == '' else cap_word(p) for p in parts))
    return {"outputs": out}
