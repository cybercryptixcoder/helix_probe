def predict(probe):
    # Leading whitespace stripped before any check [E4, E6, E7]
    # "Hello" is replaced by "ello" wherever it occurs [E1, E4, E5, E6]
    # "HELLO" is replaced by "ELLO" wherever it occurs [E8]
    # Trailing whitespace stripped [E3, E5, E6, E7]
    # Other capitalizations (hELLo) unchanged [E8]
    out = []
    for s in probe["inputs"]:
        s = s.lstrip()
        s = s.replace("Hello", "ello")
        s = s.replace("HELLO", "ELLO")
        s = s.rstrip()
        out.append(s)
    return {"outputs": out}
