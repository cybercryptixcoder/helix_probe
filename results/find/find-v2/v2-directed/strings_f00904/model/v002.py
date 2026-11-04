def predict(probe):
    # The box reverses the string [E1, E2, E3]
    # Exception: in "Hello, World" -> "dlror ,olleH", the 'W' became 'r' [E3]
    #   i.e. 'W' maps to 'r' somewhere in the process. Only one data point,
    #   so treat as: uppercase 'W' is replaced by 'r' before/after reversal? [E3, ?]
    # All other characters reverse normally, case preserved [E1, E2, E3]
    def f(s):
        # 'W' -> 'r' substitution observed in E3 ("Hello, World" -> "dlror ,olleH")
        s = s.replace("W", "r")
        return s[::-1]
    return {"outputs": [f(s) for s in probe["inputs"]]}
