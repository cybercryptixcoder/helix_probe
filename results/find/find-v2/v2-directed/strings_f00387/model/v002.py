def predict(probe):
    # Mechanism inferred:
    # 1) Capitalize the first character of the string [E1: hello->Hello, 123->123 unchanged]
    # 2) Delete every lowercase 'm' everywhere in the string [E3: good morning -> Good orning,
    #    E4: m->"", am->A, man->An, moon->Oon, memory->Eory, summer->Suer, m m m->"  "]
    # 3) The deletion happens BEFORE capitalization? Check E4: "morning" -> "Orning".
    #    If delete first: "orning" -> capitalize -> "Orning". Yes.
    #    "man" -> delete m -> "an" -> "An". Yes.
    #    "m" -> "" -> "". Yes.
    # 4) Capitalization only uppercases first char if it is a lowercase letter;
    #    digits/symbols/space unchanged [E1: 123->123, "a b c"->"A b c"].
    # 5) Only lowercase 'm' is deleted; uppercase 'M'? No evidence, assume only lowercase 'm'
    #    since all evidence uses lowercase. "HELLO WORLD"->"Hello world" (no m).
    #    E2 "123 ABC" -> "123 abc": first char '1' unchanged, rest lowercased? Wait!
    #    Check: "123 ABC" -> "123 abc". That means after first char, the rest is LOWERCASED.
    #    But E1 "Hello" -> "Hello" (rest already lowercase). "HELLO" -> "Hello" (rest lowercased).
    #    E2 "hello WORLD" -> "Hello world". Yes! So the rule is:
    #    - Delete lowercase 'm's
    #    - Uppercase first char, LOWERCASE the rest.
    #    Check E3 "hello, world" -> "Hello, world" (rest lowercased, already lower).
    #    E1 "A1!" not given but "abc"->"Abc", "123"->"123".
    #    E2 "xYz 123" -> "Xyz 123": delete m (none), first upper, rest lower. Yes.
    # 6) Order: delete m first, then capitalize-first/lowercase-rest.
    #    "morning": delete m -> "orning" -> "Orning". Yes.
    #    "m": "" -> "". Yes.
    #    "am": "a" -> "A". Yes.
    #    "memory": "eory" -> "Eory". Yes.
    #    "summer": "suer" -> "Suer". Yes.
    #    "m m m": "  " -> first char space (not letter, unchanged), rest lowercased -> "  ". Yes.
    # 7) Lowercase rest: E2 "HELLO WORLD" -> "Hello world" confirms rest lowercased.
    #    E1 "HELLO" -> "Hello". Yes.
    # Edge: what about non-ASCII? Use Python .lower()/.upper() on first char.

    def transform(s):
        # delete lowercase 'm'
        s = s.replace('m', '')
        if not s:
            return s
        first = s[0]
        # uppercase first char if it's a letter (lowercase letter -> upper)
        if first.islower():
            first = first.upper()
        # lowercase the rest
        rest = s[1:].lower()
        return first + rest

    inputs = probe.get("inputs", [])
    outputs = []
    for x in inputs:
        try:
            outputs.append(transform(x))
        except Exception:
            outputs.append("")
    return {"outputs": outputs}
