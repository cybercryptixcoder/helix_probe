def predict(probe):
    # Reverse each whitespace-separated token, keep separators/order [E1,E2,E3]
    # "two words"->"owt sdr", "a b c"->"a cb", "ab cd ef"->"ba fedc" [E2]
    # "test case"->"set ac", "banana data banana "->"nab td" [E3]
    # "Hello World function lazy"->"oleH yzaitcnufdrW" [E1]
    # "banana"->"nab", "level"->"vel", "Zebra"->"arbeZ" [E1,E3]
    # "abc123"->"321cba", "Example123"->"321elpmaxE" [E1,E3]
    # " Zebralower"->"wolarbeZ" (leading space dropped) [E1]
    out = []
    for s in probe.get("inputs", []):
        try:
            out.append(" ".join(w[::-1] for w in s.split() if w))
        except Exception:
            out.append("")
    return {"outputs": out}
