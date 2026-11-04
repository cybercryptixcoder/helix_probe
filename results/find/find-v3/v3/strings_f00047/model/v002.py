def predict(probe):
    # Only the first letter of the entire string is uppercased; rest lowercased [E1, E2]
    # "Hello World function lazy" -> "Hello world function lazy" [E1]
    # "MiXeD CaSe words" -> "Mixed case words" [E2]
    # "  two  spaces" -> "  two  spaces" (leading spaces: first char is space, unchanged) [E2]
    # "a b c" -> "A b c" [E2]
    # "123abc" -> "123abc" (first char digit, unchanged) [E2]
    outs = []
    for s in probe["inputs"]:
        if not s:
            outs.append(s)
        else:
            outs.append(s[0].upper() + s[1:].lower())
    return {"outputs": outs}
