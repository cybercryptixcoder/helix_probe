def predict(probe):
    # Strip whitespace from both ends of the ORIGINAL string first [E2, E4, E8, E10]
    #   - "aH H" -> "a " (not "a"), proving strip precedes H-removal [E10]
    #   - "  H  " -> "" shows full strip of surrounding whitespace [E8]
    #   - \t, \n, \u00a0 are all stripped [E12]
    # Then remove every uppercase 'H' character [E2, E6, E8, E10]
    #   - lowercase 'h' is preserved ("hello"->"hello", "hH"->"h") [E6]
    #   - internal spaces are preserved ("aH H b"->"a  b") [E8]
    outputs = []
    for s in probe["inputs"]:
        t = s.strip()
        t = t.replace("H", "")
        outputs.append(t)
    return {"outputs": outputs}
