def predict(probe):
    # Identity for most inputs [E1, E2]
    # Exception: the substring "spaces" becomes "skaces" [E2]
    # Exception: the substring "ple" becomes "kle" [E3: "Example123" -> "Examkle123"]
    #   - "Example123" -> "Examkle123" (ple -> kle)
    #   - "level" unaffected (no "ple")
    #   - "banana", "lazy", "test case" unaffected
    # Best guess: replace "spaces"->"skaces" and "ple"->"kle".
    # Note: "spaces" contains no "ple"; order of replacement doesn't matter here.
    def f(s):
        s = s.replace("spaces", "skaces")
        s = s.replace("ple", "kle")
        return s
    return {"outputs": [f(s) for s in probe["inputs"]]}
