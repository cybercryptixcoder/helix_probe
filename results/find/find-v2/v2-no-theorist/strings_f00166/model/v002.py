def predict(probe):
    # Identity for most inputs [E1, E2]
    # Exception: the substring "spaces" becomes "skaces" [E2]
    #   - "  leading spaces" -> "  leading skaces"
    #   - "trailing spaces  " -> "trailing skaces  "
    #   - "hello world", "foo  bar", etc. unaffected
    # Best guess: replace every occurrence of "spaces" with "skaces".
    return {"outputs": [s.replace("spaces", "skaces") for s in probe["inputs"]]}
