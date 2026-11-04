def predict(probe):
    # Whole string lowercased, first char title-cased: exactly str.capitalize() [E10]
    #   ß->Ss, ﬁ->Fi, ǅ stays ǅ, Ǆ->ǅ, final sigma ς preserved [E10]
    # Then remove all whitespace [E1,E3]
    # Capitalization tied to raw first char, even if it is whitespace [E7,E8]
    out = []
    for s in probe.get("inputs", []):
        out.append("".join(s.capitalize().split()))
    return {"outputs": out}
