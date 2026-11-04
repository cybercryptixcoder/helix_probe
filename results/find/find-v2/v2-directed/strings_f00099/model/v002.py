def predict(probe):
    # f reverses the whole string character by character [E1, E2]
    # Case preserved [E1: Hello->olleH]
    # BUT leading spaces are stripped before reversing, trailing spaces preserved [E2]
    #   "  hello world  " -> "dlrow olleh  " (leading spaces gone, trailing kept)
    #   "trailing space " -> "ecaps gniliart" (trailing space gone here? no: input ends with space)
    #   Wait: "trailing space " reversed = " ecaps gniliart"; observed "ecaps gniliart" -> trailing space stripped
    # So: strip leading whitespace, then reverse? Check "  hello world  ": strip leading -> "hello world  ", reverse -> "  dlrow olleh". No.
    # Observed "dlrow olleh  ": that's reverse of "  hello world" (strip trailing). 
    # "trailing space " -> "ecaps gniliart" = reverse of "trailing space" (strip trailing space).
    # So trailing whitespace is stripped, then reversed. Leading spaces then end up trailing in output.
    # Check "  hello world  ": strip trailing -> "  hello world", reverse -> "dlrow olleh  ". Matches!
    # E1 "hello  world" -> "dlrow  olleh" no trailing space, fine.
    try:
        return {"outputs": [s.rstrip()[::-1] for s in probe["inputs"]]}
    except Exception:
        return {"outputs": []}
